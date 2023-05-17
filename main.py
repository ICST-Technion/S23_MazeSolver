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
from picamera import PiCamera
from time import sleep

class MazeManager(object):
    def __init__(self, mi):
        self._mi = mi

        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        self.is_capturing = False
        self.a = None
        self.maze_env = None

    def load_env(self):
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
        self.maze_env.load_image(Config.image_file)

    def take_image(self):
        camera = PiCamera()
        camera.resolution = Config.camera_resolution
        camera.start_preview()
        sleep(4)

        while self.is_capturing:
            # Camera warm-up time
            camera.capture(Config.image_file)
            sleep(1)

    def start_capture(self):
        self.is_capturing = True
        t = threading.Thread(target=self.take_image)
        t.start()

    def stop_capture(self):
        self.is_capturing = False

    def update(self):
        self.reload_image()
        return self.get_directions()



if __name__ == "__main__":
    # m = MazeImage(Config.image_file, Config.aruco_dict)
    # subprocess.call(['raspistill', '-o', Config.image_file])
    m = MazeImage(Config.image_file, Config.aruco_dict)
    input("Press Enter when ready")
    manager = MazeManager(m)
    manager.take_image()
    manager.load_env()
    manager.start_capture()
    s = DirectionsServer(Config.host, Config.port, manager)
    s.start_server()

    # maze_env.print_maze()
    #
    # cv2.destroyAllWindows()  # destroy all windows
