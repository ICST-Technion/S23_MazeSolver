import cv2
import sys

import numpy as np

from Camera.camera import Camera
from config import Config
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent, ContextHeuristic
from Server.server import DirectionsServer, ControlServer
import logging
import time
import threading
from distance_calibration.confidence_based import ConfidenceCalibrator
import math
from Robot.robot import Robot

def dist(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 +
              (c1[1] - c2[1]) ** 2)


def size(a):
    return np.sqrt(a[0]**2 + a[1]**2)


def get_height_point_to_line(a, b, p):
    return np.dot(np.array([b[0] - a[0], b[1] - a[1]]), np.array(b[0] - p[0], b[1]-p[1]))/(dist(a, b)*dist(b, p))


class MazeManager(object):
    def __init__(self):
        self.last_action = "UP"
        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        self.cam = Camera(frame_rate=Config.frame_rate, camera_resolution=Config.camera_resolution)
        self._mi = MazeImage(Config.aruco_dict)
        self.agent = None
        self.maze_env = None
        self.stopped = True
        self.robot = Robot(Config.kp, Config.ki, Config.kd)
        self.confidence_model = ConfidenceCalibrator(Config.lower_confidence_thresh)
        self.movement_coef = 1
        self.server = DirectionsServer(Config.host, Config.port, self)
        self.control_server = ControlServer(Config.host, Config.port, self)
        self.last_interval = 0
        self.directions = []
        self.cords = []
        self.last_turn = (0, 0)
        self.status = {
            "connection": True,
            "path_found": False,
            "running": False,
            "calculating_path": False,}

    def get_status(self):
        return self.status

    def get_image(self):
        return self.maze_env.get_image()

    def is_stopped(self):
        return self.stopped

    def stop_solver(self):
        self.stopped = True
        self.status['running'] = False

    def start_solver(self):
        self.stopped = False
        self.status['running'] = True

    def reload_initial_image(self):
        self.stopped = True
        self.maze_env.load_initial_image(self.cam.retrieve_image())

    def load_env(self):
        self.stopped = True
        # loads maze without aruco
        self._mi.load_initial_image(self.cam.retrieve_image())
        # waits for user to start
        while self.stopped:
            time.sleep(1)
        # loads maze with aruco
        self._mi.load_aruco_image(self.cam.retrieve_image())
        self.maze_env = MazeSearchEnv(self._mi)
        self.agent = WeightedAStarAgent(self.maze_env, 0.5, Heuristic1())
        self.update_directions()

    def update_directions(self):
        self.server.updating_started()
        self.status['calculating_path'] = True
        self.reload_image()
        self.directions = self.get_directions()
        print(self.directions)
        self.status['calculating_path'] = False
        self.server.finished_updating()

    def reload_image(self):
        self.maze_env.load_image(self.cam.retrieve_image())

    def get_current_coords(self):
        self.reload_image()
        current_cords = self.maze_env.get_current_coords()
        return current_cords

    def get_last_coords(self):
        return self.maze_env.get_current_coords()

    def update_parameters(self, expected, actual, current, last):
        if dist(last, current) > Config.moved_sensitivity:
            self.movement_coef = expected/actual

    def init_capture(self):
        self.cam.start_live_capture()

    def stop_capture(self):
        self.cam.stop_live_capture()

    def start_server(self, blocking=False):
        if blocking:
            self.server.start_server()
        else:
            t = threading.Thread(target=self.server.start_server)
            t.start()

    def start_control_server(self, blocking=False):
        if blocking:
            self.server.start_server()
        else:
            t = threading.Thread(target=self.control_server.start_server)
            t.start()

    def get_directions(self):
        actions, cost, expanded = self.agent.run_search()
        cords = self.maze_env.actions_to_cords(actions)
        # added to improve A star times
        self.agent.heuristic = ContextHeuristic(cords)
        if cost == -1:
            self.status['path_found'] = False
            return []
        else:
            self.status['path_found'] = True
            print("got cost: ", cost)
            logging.debug(f"found path: {cost != -1}")
            smoothed_actions = self.process_actions(actions)
            self.cords = self.maze_env.actions_to_cords_with_weight(smoothed_actions)
            self.last_turn = self.cords.pop(0)
            return smoothed_actions

    def get_car_angle(self):
        return self.maze_env.get_car_angle()

    def process_actions(self, actions):
        new_actions = []
        counter = 0
        action_type = actions[0]

        for a in actions:
            if a != action_type:
                if counter > Config.min_actions_for_movement:
                    if new_actions and new_actions[-1][0] == action_type:
                        new_item = (new_actions[-1][0], new_actions[-1][1] + counter)
                        new_actions.pop()
                        new_actions.append(new_item)
                    else:
                        new_actions.append((action_type, counter))
                action_type = a
                counter = 1
            else:
                counter += 1
        return new_actions

    def get_next_direction(self):
        if not self.directions:
            return Config.actions_to_num["STAY"], 0, 0, 0
        action = self.directions[0][0]
        amount = min(self.directions[0][1], Config.interval_size)

        if action == self.last_action:
            self.last_interval = amount
            temp = (action, self.directions[0][1] - amount)
            self.directions[0] = temp
            if self.directions[0][1] <= 0:
                self.directions.pop(0)
            speed_l, speed_r = self.robot.get_speeds()
            return Config.actions_to_num["UP"], speed_l, speed_r, int(self.movement_coef * amount)
        else:
            if self.last_action == "UP":
                if action == "RIGHT":
                    self.last_action = "RIGHT"
                    return Config.actions_to_num["RIGHT"], 0, 0, Config.right_angle
                if action == "LEFT":
                    self.last_action = "LEFT"
                    return Config.actions_to_num["LEFT"], 0, 0, Config.right_angle

            if self.last_action == "RIGHT":
                if action == "UP":
                    self.last_action = "UP"
                    return Config.actions_to_num["LEFT"], 0, 0, Config.right_angle
                if action == "DOWN":
                    self.last_action = "DOWN"
                    return Config.actions_to_num["RIGHT"], 0, 0,  Config.right_angle

            if self.last_action == "LEFT":
                if action == "UP":
                    self.last_action = "UP"
                    return Config.actions_to_num["RIGHT"], 0, 0,  Config.right_angle
                if action == "DOWN":
                    self.last_action = "DOWN"
                    return Config.actions_to_num["LEFT"], 0, 0,  Config.right_angle

            if self.last_action == "DOWN":
                if action == "RIGHT":
                    self.last_action = "RIGHT"
                    return Config.actions_to_num["LEFT"], 0, 0, Config.right_angle
                if action == "LEFT":
                    self.last_action = "LEFT"
                    return Config.actions_to_num["RIGHT"], 0, 0,  Config.right_angle

    def update_step(self):
        # if we have directions left
        if self.directions:
            last_loc = self.get_last_coords()
            current_location = self.get_current_coords()

            # update sideways position
            err = get_height_point_to_line(self.last_turn, self.cords[0], current_location)
            self.robot.calc_speeds(err)

            # update forward coefficient and update directions if was off
            num_expected = self.last_interval
            num_traveled = dist(last_loc, current_location)

            self.confidence_model.update(num_expected, num_traveled)
            if self.confidence_model.to_update():
                self.update_parameters(num_expected, num_traveled, current_location, last_loc)
                self.update_directions()
                time.sleep(0.1)


if __name__ == "__main__":
    manager = MazeManager()
    manager.init_capture()
    time.sleep(0.5)
    manager.cam.save_image("saved.jpg")
    manager.load_env()
    manager.start_control_server(blocking=False)
    manager.start_server(blocking=True)
