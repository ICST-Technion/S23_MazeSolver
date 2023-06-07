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


def get_distance_left(current_loc, src, dst):
    if src[0] == dst[0]:
        if src[1] <= current_loc[1] <= dst[1] or dst[1] <= current_loc[1] <= src[1]:
            print("1")
            return dist(current_loc, dst)
        else:
            print("2")
            return -dist(current_loc, dst)
    else:
        if src[0] <= current_loc[0] <= dst[0] or dst[0] <= current_loc[0] <= src[0]:
            print("3")
            return dist(current_loc, dst)
        else:
            print("4")
            return -dist(current_loc, dst)


def calculate_cos_theta(point1, point2):
    angle_1 = 180*np.arctan2(point1[0], point1[1])/np.pi
    angle_2 = 180*np.arctan2(point2[0], point2[1])/np.pi
    print(f"a1: {angle_1} a2: {angle_2}")
    return angle_1 - angle_2


def size(a):
    return np.sqrt(a[0] ** 2 + a[1] ** 2)


def distance_from_line(line_point1, line_point2, point):
    # Calculate the direction vector of the line
    line_direction = (line_point2[0] - line_point1[0], line_point2[1] - line_point1[1])

    # Calculate the vector from the line point to the given point
    line_to_point_vector = (point[0] - line_point1[0], point[1] - line_point1[1])

    # Calculate the magnitude of the line direction vector
    line_direction_magnitude = math.sqrt(line_direction[0] ** 2 + line_direction[1] ** 2)

    # Calculate the projection of the line-to-point vector onto the line direction vector
    projection = (
            (line_to_point_vector[0] * line_direction[0] + line_to_point_vector[1] * line_direction[1])
            / line_direction_magnitude
    )

    # Calculate the projection vector
    projection_vector = (projection * line_direction[0] / line_direction_magnitude,
                         projection * line_direction[1] / line_direction_magnitude)

    # Calculate the distance vector from the line to the point
    distance_vector = (line_to_point_vector[0] - projection_vector[0],
                       line_to_point_vector[1] - projection_vector[1])

    # Calculate the distance from the line to the point
    distance = math.sqrt(distance_vector[0] ** 2 + distance_vector[1] ** 2)

    # Check which side of the line the point is on
    side = (line_to_point_vector[0] * line_direction[1] -
            line_to_point_vector[1] * line_direction[0])

    if side > 0:
        distance *= -1  # One side is considered negative

    return distance


class MazeManager(object):
    def __init__(self):
        self.last_action = "RIGHT"
        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        self.cam = Camera(frame_rate=Config.frame_rate, camera_resolution=Config.camera_resolution)
        self._mi = MazeImage(Config.aruco_dict)
        self.agent = None
        self.maze_env = None
        self.stopped = True
        self.robot = Robot(Config.kp, Config.ki, Config.kd, Config.a_kp, Config.a_ki, Config.a_kd)
        self.confidence_model = ConfidenceCalibrator(Config.lower_confidence_thresh)
        self.movement_coef = 10
        self.server = DirectionsServer(Config.host, Config.port, self)
        self.control_server = ControlServer(Config.host, Config.webserver_port, self)
        self.last_interval = 0
        self.moved_forward = False
        self.directions = []
        self.cords = []
        self.is_rotating = False
        self.last_turn = [0, 0]
        self.status = {
            "connection": True,
            "path_found": False,
            "running": False,
            "calculating_path": False, }

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

    def load_env(self, from_file=False):
        self.stopped = True
        # loads maze without aruco
        if from_file:
            im = cv2.imread(Config.image_file, cv2.IMREAD_GRAYSCALE)
        else:
            im = self.cam.retrieve_image()
        self._mi.load_initial_image(im)
        # waits for user to start
        while self.stopped:
            time.sleep(1)
        # loads maze with aruco
        self._mi.load_aruco_image(self.cam.retrieve_image())
        self.maze_env = MazeSearchEnv(self._mi)
        self.agent = WeightedAStarAgent(self.maze_env, 0.5, Heuristic1())
        self.update_directions()

    def update_directions(self):
        print("updating directions")
        changed_stop = False
        if not self.stopped:
            self.stopped = True
            changed_stop = True
        self.server.updating_started()
        self.status['calculating_path'] = True
        self.reload_image()
        self.directions = self.get_directions()
        print(self.directions)
        self.status['calculating_path'] = False
        self.server.finished_updating()
        if changed_stop:
            self.stopped = False

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
            print("updated coef:", expected / actual)
            self.movement_coef = (expected / actual) * self.movement_coef

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
        if cost == -1:
            self.status['path_found'] = False
            return []
        else:
            cords = self.maze_env.actions_to_cords(actions)

            # added to improve A star times
            self.agent.heuristic = ContextHeuristic(cords)
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

    def get_dynamic_next_direction(self):
        if not self.directions:
            print("ran out")
            return Config.actions_to_num["STAY"], 0, 0, 0

        if self.is_rotating:
            print("got to rotate")
            try:
                rot_vec = (self.cords[0][0] - self.last_turn[0], self.cords[0][1]-self.last_turn[1])
                err = calculate_cos_theta(rot_vec, self.maze_env.get_direction_vector())
            except Exception as e:
                print(e)
            print(f"got rotate err: {err}")
            amount = self.robot.get_rotation_length(err)
            print(f"rotating for: {amount}")
            if amount > 0:
                return Config.actions_to_num["RIGHT"], Config.rotation_speed, Config.rotation_speed, abs(int(amount))
            if amount < 0:
                return Config.actions_to_num["LEFT"], Config.rotation_speed, Config.rotation_speed, abs(int(amount))
            return Config.actions_to_num["STAY"], 0, 0, int(0)
        else:
            if self.directions[0][1] > 0:
                amount = min(self.directions[0][1], Config.interval_size)
                print(f"moving forward: {amount} pixels")
                self.moved_forward = True
                self.last_interval = amount
                speed_l, speed_r = self.robot.get_speeds()
                return Config.actions_to_num["UP"], speed_l, speed_r, int(self.movement_coef * amount)
            else:
                amount = min(-self.directions[0][1], Config.interval_size)
                print(f"moving backward: {amount} pixels")
                self.moved_forward = True
                self.last_interval = amount
                speed_l, speed_r = self.robot.get_speeds()
                return Config.actions_to_num["DOWN"], speed_r, speed_l, int(self.movement_coef * amount)

    def update_step(self):
        # if we have directions left
        if self.directions:
            print(self.directions)
            print(self.cords)
            print(f"new direction: {self.directions[0]} current cord: {self.cords[0]} last cord: {self.last_turn} ")
            # gets current and last location and updates current location
            last_loc = self.get_last_coords()
            current_location = self.get_current_coords()
            print(f"current location: {current_location}")
            # if rotating
            if self.is_rotating:
                rot_vec = (self.cords[0][0] - self.last_turn[0], self.cords[0][1]-self.last_turn[1])
                err = calculate_cos_theta(rot_vec, self.maze_env.get_direction_vector())
                # if we are off by less than sensitivity then stop rotation
                if abs(err) < Config.rotation_sensitivity:
                    print("finished rotating")
                    self.is_rotating = False
                    # starting forward movement so reset old errors
                    self.robot.reset_dir_pid()
            else:
                # update sideways position
                err = distance_from_line(self.last_turn, self.cords[0], current_location)
                if err < 0:
                    err = min(err+5, 0)
                if err > 0:
                    err = max(err-5, 0)
                print("forward error:", err)
                self.robot.calc_speeds(err)
                # update forward coefficient and update directions if was off
                num_expected = self.last_interval
                num_traveled = dist(last_loc, current_location)
                print(f"num_expected {num_expected} num_traveled: {num_traveled}")
                if self.moved_forward:
                    # update the amount to move the amount left
                    print(f"distance left: {get_distance_left(current_location, self.last_turn, self.cords[0])}")
                    temp = (self.directions[0][0], get_distance_left(current_location, self.last_turn, self.cords[0]))
                    self.directions[0] = temp
                    # if we moved past or to the point we needed
                    # TODO: consider checking if really negative then recalculate maze path
                    if abs(self.directions[0][1]) <= Config.accuracy_threshold:
                        self.directions.pop(0)
                        self.last_turn = self.cords.pop(0)
                        # we finished moving in direction then start rotation
                        self.is_rotating = True
                        # just started rotating so reset old errors
                        self.robot.reset_angle_pid()
                        print(f"popped direction")
                    self.update_parameters(num_expected, num_traveled, current_location, last_loc)
        else:
            self.update_directions()


if __name__ == "__main__":
    manager = MazeManager()
    manager.init_capture()
    time.sleep(0.5)
    # manager.cam.save_image("saved.jpg")
    manager.start_control_server(blocking=False)
    manager.load_env(from_file=True)
    manager.start_server(blocking=True)
