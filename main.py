import cv2
import sys
from config import Config
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent, ContextHeuristic
from Server.server import DirectionsServer
import logging
import subprocess
import threading
from distance_calibration.confidence_based import PIDController, ConfidenceCalibrator
from picamera import PiCamera
from time import sleep
import numpy as np

class MazeManager(object):
    def __init__(self, mi, live_capture = False):
        self._mi = mi

        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        self.is_capturing = False
        self.live_capture = live_capture
        self.a = None
        self.maze_env = None
        self.picture_lock = threading.Lock()
        self.image = np.empty((Config.camera_resolution[1], Config.camera_resolution[0]), dtype=np.uint8)


    def load_env(self):
        if self.live_capture:
            self._mi.load_aruco_image(self.image, from_arr=True)
        else:
            self._mi.load_aruco_image(Config.image_file)
        self.maze_env = MazeSearchEnv(self._mi)
        self.a = WeightedAStarAgent(self.maze_env, 0.5, Heuristic1())


    def get_directions(self):
        actions, cost, expanded = self.a.run_search()
        cords = self.maze_env.actions_to_cords(actions)
        # added to improve A star times
        self.a.heuristic = ContextHeuristic(cords)
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

    def reload_image(self):
        if self.live_capture:
            self.maze_env.load_image(self.image, from_arr=True)
        else:
            self.maze_env.load_image(Config.image_file)

    def take_image(self):
        camera = PiCamera()
        camera.resolution = Config.camera_resolution
        while self.is_capturing:
            # Camera warm-up time
            self.picture_lock.acquire(blocking=True)
            if self.live_capture:
                camera.capture(self.image, 'gray')
            else:
                camera.capture(Config.image_file)
            sleep(0.3)
            self.picture_lock.release()

    def start_capture(self):
        self.is_capturing = True
        t = threading.Thread(target=self.take_image)
        t.start()

    def stop_capture(self):
        self.is_capturing = False

    def get_current_coords(self):
        self.picture_lock.acquire(blocking=True)
        self.reload_image()
        self.picture_lock.release()
        return self.maze_env.get_current_coords()

    def update(self):
        self.picture_lock.acquire(blocking=True)
        self.reload_image()
        self.picture_lock.release()
        return self.get_directions()

    def get_new_position(self, curr, action, val):
        return self.maze_env.get_new_position(curr, action, val)



if __name__ == "__main__":
    # m = MazeImage(Config.image_file, Config.aruco_dict)
    subprocess.call(['raspistill', '-o', Config.image_file])
    m = MazeImage(Config.image_file, Config.aruco_dict)
    input("Press Enter when ready")
    manager = MazeManager(m, live_capture=True)
    manager.start_capture()
    sleep(5)
    manager.load_env()
    p = PIDController(Config.pv, Config.iv, Config.dv)
    c = ConfidenceCalibrator(p)
    s = DirectionsServer(Config.host, Config.port, manager, c)
    s.start_server()

    # maze_env.print_maze()
    #
    # cv2.destroyAllWindows()  # destroy all windows
