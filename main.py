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

    def update(self):
        self.reload_image()
        return self.get_directions()



if __name__ == "__main__":
    m = MazeImage(Config.image_file, Config.aruco_dict)
    # manager = MazeManager()

    # s = DirectionsServer(Config.host, Config.port, manager)
    # s.start_server()

    # maze_env.print_maze()
    #
    # cv2.destroyAllWindows()  # destroy all windows
