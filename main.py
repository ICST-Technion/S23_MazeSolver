import cv2
import sys
from config import Config
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent
from Server.server import DirectionsServer
import logging

class MazeManager(object):
    def __init__(self):
        self.maze_env = MazeSearchEnv(Config.image_file, Config.aruco_dict)
        self.a = WeightedAStarAgent(self.maze_env, 0.5, Heuristic1())
        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)

    def get_directions(self):
        actions, cost, expanded = self.a.run_search()
        logging.debug(f"found path: {cost != -1}")
        return actions

    def reload_image(self):
        self.maze_env.load_image(Config.image_file)

    def update(self):
        self.reload_image()
        return self.get_directions()



if __name__ == "__main__":
    # m = MazeImage(Config.image_file, Config.aruco_dict)
    m = MazeManager()
    s = DirectionsServer(Config.host, Config.port, m)
    s.start_server()

    # maze_env.print_maze()
    #
    # cv2.destroyAllWindows()  # destroy all windows
