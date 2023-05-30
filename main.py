import cv2
import sys

from Camera.camera import Camera
from config import Config
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent, ContextHeuristic
from Server.server import DirectionsServer
import logging
import time
import threading
from distance_calibration.confidence_based import PIDController, ConfidenceCalibrator
from time import sleep
import math

def dist(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 +
              (c1[1] - c2[1]) ** 2)


class MazeManager(object):
    def __init__(self):
        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        self.cam = Camera(frame_rate=Config.frame_rate, camera_resolution=Config.camera_resolution)
        self._mi = MazeImage(Config.aruco_dict)
        self.agent = None
        self.maze_env = None
        self.pid_controller_f = PIDController(Config.pv, Config.iv, Config.dv)
        self.pid_controller_s = PIDController(Config.pv, Config.iv, Config.dv)
        self.confidence_controller_forward = ConfidenceCalibrator(self.pid_controller_f)
        self.movement_coef = 1
        self.server = DirectionsServer(Config.host, Config.port, self)
        self.directions = []
        self.last_movement = 0
        self.last_action = 'UP'


    def load_env(self):
        # loads maze without aruco
        self._mi.load_initial_image(self.cam.retrieve_image())
        input("press enter to continue")
        # loads maze with aruco
        self._mi.load_aruco_image(self.cam.retrieve_image())
        self.maze_env = MazeSearchEnv(self._mi)
        self.agent = WeightedAStarAgent(self.maze_env, 0.5, Heuristic1())
        self.update_directions()

    def update_directions(self):
        self.server.updating_started()
        self.reload_image()
        self.directions = self.get_directions()
        self.server.finished_updating()

    def reload_image(self):
        self.maze_env.load_image(self.cam.retrieve_image(), from_arr=True)

    def get_current_coords(self):
        self.reload_image()
        current_cords = self.maze_env.get_current_coords()
        return current_cords

    def get_last_coords(self):
        return self.maze_env.get_current_coords()

    def update_parameters(self, forward_error):
        last_coords = self.maze_env.get_current_coords()
        current_coords = self.get_current_coords()
        # vehicle moved
        if dist(last_coords, current_coords) > Config.moved_sensitivity:
            forward_pid = self.confidence_controller_forward.calibrate(forward_error)
            self.movement_coef += Config.learning_rate * forward_pid

    def init_capture(self):
        self.cam.start_live_capture()

    def stop_capture(self):
        self.cam.stop_live_capture()

    def start_server(self, blocking=False):
        if blocking:
            self.start_server()
        else:
            t = threading.Thread(target=self.start_server)
            t.start()

    def get_directions(self):
        actions, cost, expanded = self.agent.run_search()
        cords = self.maze_env.actions_to_cords(actions)
        # added to improve A star times
        self.agent.heuristic = ContextHeuristic(cords)
        print("got cost: ", cost)
        logging.debug(f"found path: {cost != -1}")
        return self.process_actions(actions)

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

    def get_new_position(self, curr, action, val):
        return self.maze_env.get_new_position(curr, action, val)

    def get_next_direction2(self):
        action = self.directions[0][0]
        if action == self.last_action:
            direction = self.directions.pop(0)
            self.last_movement = int(direction[1])
            self.last_action = direction[0]
            return Config.actions_to_num["UP"], self.movement_coef*int(direction[1])
        else:
            direction = self.directions[0]
            if self.last_action == "UP":
                if direction[0] == "RIGHT":
                    self.last_action = "RIGHT"
                    return Config.actions_to_num["RIGHT"],  680
                if direction[0] == "LEFT":
                    self.last_action = "LEFT"
                    return Config.actions_to_num["LEFT"], 680

            if self.last_action == "RIGHT":
                if direction[0] == "UP":
                    self.last_action = "UP"
                    return Config.actions_to_num["LEFT"],  680
                if direction[0] == "DOWN":
                    self.last_action = "DOWN"
                    return Config.actions_to_num["RIGHT"],  680

            if self.last_action == "LEFT":
                if direction[0] == "UP":
                    self.last_action = "UP"
                    return Config.actions_to_num["RIGHT"],  680
                if direction[0] == "DOWN":
                    self.last_action = "DOWN"
                    return Config.actions_to_num["LEFT"],  680

            if self.last_action == "DOWN":
                if direction[0] == "RIGHT":
                    self.last_action = "RIGHT"
                    return Config.actions_to_num["LEFT"],  680
                if direction[0] == "LEFT":
                    self.last_action = "LEFT"
                    return Config.actions_to_num["RIGHT"],  680


    def get_next_direction(self):
        action = self.directions[0][0]
        angle = self.get_car_angle()
        if (abs(angle - Config.angle_map[action])) > Config.rotation_sensitivity:
            diff = angle - Config.angle_map[action]
            rotate_dir = "LEFT" if diff < 0 else "RIGHT"
            if abs(diff) > 180:
                if rotate_dir == "LEFT":
                    rotate_dir = "RIGHT"
                    diff = 360 - abs(diff)
                else:
                    rotate_dir = "LEFT"
                    diff = 360 - abs(diff)
            return Config.actions_to_num[rotate_dir], int(abs(diff))
        direction = self.directions.pop(0)
        self.last_movement = int(direction[1])
        return Config.actions_to_num["UP"],  self.movement_coef*int(direction[1])

    def update_step(self):
        last_loc = self.get_last_coords()
        current_location = self.get_current_coords()
        # if moved and not updating currently
        if dist(last_loc, current_location) > Config.moved_sensitivity and not self.server.lock.locked():
            num_expected = self.last_movement
            num_traveled = dist(last_loc, current_location)
            forward_error = num_expected - num_traveled
            self.update_parameters(forward_error)
            if self.confidence_controller_forward.to_update():
                t = threading.Thread(target=self.update_directions)
                t.start()
                time.sleep(0.1)


    def main_loop(self):
        while True:
            # if reached destination
            self.update_step()

if __name__ == "__main__":
    manager = MazeManager()
    manager.init_capture()
    time.sleep(0.5)
    manager.load_env()
    manager.start_server(blocking=True)

    # maze_env.print_maze()
    #
    # cv2.destroyAllWindows()  # destroy all windows
