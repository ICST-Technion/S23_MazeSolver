import cv2
import numpy as np
import logging
import time
import threading
import math
import signal

from Camera.camera import Camera
from config import Config
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent, ContextHeuristic
from Server.server import DirectionsServer, ControlServer
from Robot.robot import Robot


def dist(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 +
                     (c1[1] - c2[1]) ** 2)


# change dist here to be L1 not L2
def get_distance_left(current_loc, src, dst, action_type):
    if src[0] == dst[0]:
        num_left = np.sign(dst[1] - current_loc[1])
        if num_left == np.sign(Config.action_vectors[action_type][1]):
            return abs(dst[1] - current_loc[1])
        else:
            return -abs(dst[1] - current_loc[1])
    else:
        num_left = np.sign(dst[0] - current_loc[0])
        if num_left == np.sign(Config.action_vectors[action_type][0]):
            return abs(dst[0] - current_loc[0])
        else:
            return -abs(dst[0] - current_loc[0])

def calculate_cos_theta(next_direction, current_direction):
    angle_1 = 180*np.arctan2(next_direction[0], next_direction[1])/np.pi
    angle_1 = (angle_1 + 360) % 360
    angle_2 = 180*np.arctan2(current_direction[0], current_direction[1])/np.pi
    angle_2 = (angle_2 + 360) % 360
    rotation_amount = min(abs(angle_1 - angle_2), abs(360 - abs(angle_1-angle_2)))
    if angle_1 == 0:
        if angle_2 > 180:
            return -rotation_amount
        else:
            return rotation_amount
    if angle_1 == 90:
        if 270 > angle_2 > 90:
            return rotation_amount
        else:
            return -rotation_amount
    if angle_1 == 180:
        if angle_2 > 180:
            return rotation_amount
        else:
            return -rotation_amount
    if angle_1 == 270:
        if 270 > angle_2 > 90:
            return -rotation_amount
        else:
            return rotation_amount
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
        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        self.cam = Camera(camera_resolution=Config.camera_resolution,
                          frame_rate=Config.frame_rate, zoom=Config.zoom)
        self._mi = MazeImage(Config.aruco_dict)
        self.agent = None
        self.maze_env = None
        self.stopped = True
        self.robot = Robot(Config.kp, Config.ki, Config.kd, Config.a_kp, Config.a_ki, Config.a_kd,
                           max_speed=Config.max_forward_speed, min_speed=Config.min_forward_speed,
                           max_rotation_speed=Config.max_rotation_speed, min_rotation_speed=Config.min_rotation_speed,
                           natural_error=Config.natural_error)
        self.movement_coef = 10
        self.rotation_err = 0
        self.server = DirectionsServer(Config.host, Config.port, self)
        self.control_server = ControlServer(Config.host, Config.webserver_port, self)
        self.last_interval = 0
        self.moved_forward = False
        self.directions = []
        self.cords = []
        self.is_rotating = True
        self.last_turn = [0, 0]
        self.finished = False
        self.is_running = True
        self.status = {
            "connection": True,
            "path_found": False,
            "running": False,
            "calculating_path": False,
            "initial_maze_loaded": False,
        }

    def get_status(self):
        """
        gets the status of the different possible operations
        :return: dict
        """
        return self.status

    def to_run(self):
        return self.is_running

    def end_run(self):
        self.is_running = False
        self.cam.stop_live_capture()

    def get_image(self):
        """
        get the current image that the maze environment is using
        :return: numpy array
        """
        return self.maze_env.get_image()

    def get_status_image(self):
        """
        gets the image to display on the app.
        specifically warped no threshold.
        if not available then the image the camera sees.
        :return: numpy array
        """
        if self.stopped:
            return self.cam.retrieve_image()
        if self.maze_env:
            return self.maze_env.get_warped_image()
        return self.cam.retrieve_image()

    def is_stopped(self):
        # returns if solver is stopped
        return self.stopped

    def stop_solver(self):
        # stops the solver
        self.stopped = True
        self.status['running'] = False

    def start_solver(self):
        # starts the solver
        self.stopped = False
        self.status['running'] = True

    def reload_initial_image(self):
        # reloads the initial image of just the maze from the camera
        self.stopped = True
        self.maze_env.load_initial_image(self.cam.retrieve_image())

    def load_env(self, from_file=False):
        """
        loads the maze env either from a file or camera's feed
        :param from_file: whether to load from file or not
        :return: None
        """
        print("1")
        self.stopped = True
        self.status['path_found'] = False
        # loads maze without aruco
        if from_file:
            im = cv2.imread(Config.image_file, cv2.IMREAD_GRAYSCALE)
        else:
            print("2")
            im = self.cam.retrieve_image()
        print("3")
        self._mi.load_initial_image(im)
        print("4")
        self.status["initial_maze_loaded"] = True

    def restart_maze(self):
        # resets maze to starting conditions and reloads directions
        try:
            self.finished = False
            self.status['calculating_path'] = True
            self.status['path_found'] = False
            self.robot.reset_angle_pid()
            self.robot.reset_dir_pid()
            self._mi.load_aruco_image(self.cam.retrieve_image())
            self.maze_env = MazeSearchEnv(self._mi)
            self.agent = WeightedAStarAgent(self.maze_env, 0.5, Heuristic1())
            self.update_directions()
            self.is_rotating = True
            self.status['calculating_path'] = False
        except:
            self.status['calculating_path'] = False


    def update_directions(self):
        """
        updates the directions of the maze from camera's image
        :return: None
        """
        changed_stop = False
        if not self.stopped:
            self.stopped = True
            changed_stop = True
        self.server.updating_started()
        self.status['calculating_path'] = True
        self.reload_image()
        self.directions = self.get_directions()
        self.status['calculating_path'] = False
        self.server.finished_updating()
        if changed_stop:
            self.stopped = False

    def reload_image(self):
        # reloads image from camera
        self.maze_env.load_image(self.cam.retrieve_image())

    def get_current_coords(self):
        # returns the current car coordinates
        # reloads image
        self.reload_image()
        current_cords = self.maze_env.get_current_coords()
        return current_cords

    def get_forward_coords(self):
        # gets the coordinates of the forward aruco on car
        self.reload_image()
        current_cords = self.maze_env.get_forward_coords()
        return current_cords

    def get_last_coords(self):
        # gets the last coordinates of the car without reloading
        return self.maze_env.get_current_coords()

    def update_parameters(self, expected, actual, current, last):
        # updates the movement coefficient if the car moved
        if dist(last, current) > Config.moved_sensitivity:
            self.movement_coef = (expected / actual) * self.movement_coef

    def init_capture(self):
        # starts live capture on the image
        self.cam.start_live_video_capture()
        # self.cam.start_live_capture()

    def stop_capture(self):
        # stops the capture
        self.cam.stop_live_capture()

    def start_server(self, blocking=False):
        # starts the commands server
        if blocking:
            self.server.start_server()
        else:
            t = threading.Thread(target=self.server.start_server)
            t.start()

    def start_control_server(self, blocking=False):
        # starts the control server
        if blocking:
            self.server.start_server()
        else:
            t = threading.Thread(target=self.control_server.start_server)
            t.start()

    def get_directions(self):
        # gets new directions by solving the maze
        actions, cost, expanded = self.agent.run_search()
        if cost == -1:
            self.status['path_found'] = False
            return []
        else:
            cords = self.maze_env.actions_to_cords(actions)
            # added to improve A star times
            self.agent.heuristic = ContextHeuristic(cords)
            self.status['path_found'] = True
            logging.debug(f"found path: {cost != -1}")
            smoothed_actions = self.process_actions(actions)

            self.cords = self.maze_env.actions_to_cords_with_weight(smoothed_actions)
            self.last_turn = self.cords.pop(0)
            return smoothed_actions

    def get_car_angle(self):
        # gets the car's angle
        return self.maze_env.get_car_angle()

    def process_actions(self, actions):
        """
        smooths out the actions of the car. Removes movements that are smaller
        than a threshold.
        :param actions: list of actions (strings)
        :return: list of actions of form (ACTION_TYPE, int)
        """
        new_actions = []
        counter = 0
        action_type = actions[0]
        for a in actions:
            if a != action_type:
                if "DIAG" in a:
                    counter += 1
                    continue
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
        """
        gets the next direction to execute.
        Stay, rotate or forward/backward.
        :return: (direction_type: int, left_speed: int, right_speed: int, duration: int)

        """
        # rot_vec = (self.cords[0][0] - self.last_turn[0], self.cords[0][1] - self.last_turn[1])
        # err = calculate_cos_theta(rot_vec, self.maze_env.get_direction_vector())
        # print(f"diff: {err}")
        # return Config.actions_to_num["STAY"], 0, 0, 0
        #
        # if not self.directions:
        #     return Config.actions_to_num["STAY"], 0, 0, 0

        if self.is_rotating:
            try:
                rot_speed = self.robot.get_rotation_speed(abs(self.rotation_err))
                if self.rotation_err > 0:
                    return Config.actions_to_num["LEFT"], rot_speed, rot_speed, Config.rotation_interval_size
                if self.rotation_err < 0:
                    return Config.actions_to_num["RIGHT"], rot_speed, rot_speed, Config.rotation_interval_size
                return Config.actions_to_num["STAY"], 0, 0, int(0)
            except Exception as e:
                print(e)
        else:
            if self.directions[0][1] > 0:
                action = Config.actions_to_num["UP"]
            else:
                action = Config.actions_to_num["DOWN"]
            amount = min(abs(self.directions[0][1]), Config.interval_size)
            self.last_interval = amount
            speed_l, speed_r = self.robot.get_speeds()
            # reduce speed if we are close to point
            print(f"speed L, R: {speed_l} , {speed_r}")
            return action, int(speed_l), int(speed_r), int(self.movement_coef * amount)

    def did_reach_end(self, current_loc):
        if dist(self.maze_env.get_end_point(), current_loc) < Config.accuracy_threshold_for_complete:
            return True
        return False

    def update_step(self):
        """
        Runs before every direction request.
        Updates:
            - current location
            - amount to travel
            - transitions from rotation/forward/backward
            - movement coeficient
            - robot speeds
        :return: None
        """
        # if we have directions left and not in stand by mode
        if self.directions and not self.stopped:
            # check if reached end
            if self.is_rotating:
                self.reload_image()
                rot_vec = (self.cords[0][0] - self.last_turn[0], self.cords[0][1]-self.last_turn[1])
                self.rotation_err = calculate_cos_theta(rot_vec, self.maze_env.get_direction_vector())
                # if we are off by less than sensitivity then stop rotation
                if abs(self.rotation_err) < Config.rotation_sensitivity:
                    self.is_rotating = False
                    self.robot.max_speed = Config.max_forward_speed
                    # starting forward movement so reset old errors
                    self.robot.reset_dir_pid()
                    self.update_step()
            else:
                current_forward_location = self.get_forward_coords()
                if self.did_reach_end(current_forward_location):
                    self.finished = True
                    return
                err = distance_from_line(self.last_turn, self.cords[0], current_forward_location)
                if err < 0:
                    err = min(err+Config.line_width/2, 0)
                if err > 0:
                    err = max(err-Config.line_width/2, 0)
                self.robot.calc_speeds(err)
                # update the amount to move to the amount left
                try:
                    current_location = self.get_current_coords()
                except:
                    print("issue with aruco")
                    self.stopped = True
                    return
                temp = (self.directions[0][0], get_distance_left(current_location, self.last_turn, self.cords[0], self.directions[0][0]))
                self.directions[0] = temp
                distance_left = self.directions[0][1]
                self.robot.update_dist_left(distance_left)
                # if we reached the point we wanted
                if abs(self.directions[0][1]) <= Config.accuracy_threshold:
                    self.directions.pop(0)
                    self.last_turn = self.cords.pop(0)
                    # we finished moving in direction then start rotation
                    self.is_rotating = True
                    # just started rotating so reset old errors
                    self.robot.reset_angle_pid()
                    self.update_step()
        else:
            self.stopped = True

    def is_finished(self):
        return self.finished


if __name__ == "__main__":
    # create manager
    manager = MazeManager()
    # start capturing images
    manager.init_capture()
    time.sleep(0.5)
    # manager.cam.save_image("saved.jpg")
    # start control server
    manager.start_control_server(blocking=False)
    manager.start_server(blocking=True)
