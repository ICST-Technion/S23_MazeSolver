import time

from config import Config
from Camera.camera import Camera
from Vehicle.vehicle import Solver
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent, ContextHeuristic
from Server.server import DirectionsServer
import logging
import subprocess
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
        self.vehicle = Solver(Config.initial_speed, Config.initial_speed, Config.learning_rate)
        self.agent = None
        self.maze_env = None
        self.pid_controller_f = PIDController(Config.pv, Config.iv, Config.dv)
        self.pid_controller_s = PIDController(Config.pv, Config.iv, Config.dv)
        self.confidence_controller_forward = ConfidenceCalibrator(self.pid_controller_f)
        self.confidence_controller_sideways = ConfidenceCalibrator(self.pid_controller_s)

        self.server = DirectionsServer(Config.host, Config.port, manager)
        self.directions = []

    def load_env(self):
        # loads maze without aruco
        self._mi.load_initial_image(self.cam.retrieve_image())
        input("press enter to continue")
        # loads maze with aruco
        self._mi.load_aruco_image(self.cam.retrieve_image())
        self.maze_env = MazeSearchEnv(self._mi)
        self.agent = WeightedAStarAgent(self.maze_env, 0.5, Heuristic1())
        self.vehicle.update_location(self.maze_env.get_current_coords())

    def get_directions(self):
        actions, cost, expanded = self.agent.run_search()
        cords = self.maze_env.actions_to_cords(actions)
        # added to improve A star times
        self.agent.heuristic = ContextHeuristic(cords)
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

    def reload_image(self):
        self.maze_env.load_image(self.cam.retrieve_image(), from_arr=True)

    def get_current_coords(self):
        self.reload_image()
        current_cords = self.maze_env.get_current_coords()
        self.vehicle.update_location(self.maze_env.get_current_coords())
        return current_cords

    def update_directions(self):
        self.server.updating_started()
        self.reload_image()
        self.directions = self.get_directions()
        self.server.finished_updating()

    def update_parameters(self, forward_error, sideways_error):
        last_coords = self.vehicle.location()
        current_coords = self.get_current_coords()
        # vehicle moved
        if dist(last_coords, current_coords) > Config.moved_sensitivity:
            forward_pid = self.confidence_controller_forward.calibrate(forward_error)
            sideways_pid = self.confidence_controller_forward.calibrate(sideways_error)
            # calibrate
            self.vehicle.update_speeds(forward_pid, sideways_pid)

    def init_capture(self):
        self.cam.stop_live_capture()

    def stop_capture(self):
        self.cam.stop_live_capture()

    def start_server(self):
        t = threading.Thread(target=self.start_server)
        t.start()

    def get_speeds(self):
        return self.vehicle.get_wheel_speeds()

    def main_loop(self):
        while True:
            # if reached destination
            self.reload_image()
            current_location = self.get_current_coords()
            if dist(self.directions[0], current_location) < Config.moved_sensitivity:
                self.directions.pop(0)

            # TODO: need to understand better if forward is x or y axis in image
            forward_error = self.directions[0] - current_location[0]
            sideways_error = self.directions[1] - current_location[1]

            self.update_parameters(forward_error, sideways_error)
            if self.confidence_controller_forward.to_update():
                self.update_directions()



if __name__ == "__main__":
    manager = MazeManager()
    manager.init_capture()
    time.sleep(0.5)
    manager.load_env()
    manager.start_server()

    # maze_env.print_maze()
    #
    # cv2.destroyAllWindows()  # destroy all windows
