import cv2
import sys
from config import Config
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent

def update_callback():
    pass

if __name__ == "__main__":
    # m = MazeImage(Config.image_file, Config.aruco_dict)
    maze_env = MazeSearchEnv(Config.image_file, Config.aruco_dict)
    a = WeightedAStarAgent(maze_env, 0.5, Heuristic1())
    print(maze_env.get_initial_state().row,maze_env.get_initial_state().col)
    actions, cost1, expanded = a.run_search()
    cv2.imshow('d', maze_env.color_maze_path_and_print(actions))
    cv2.waitKey(0)
    # maze_env.print_maze()
    #
    # cv2.destroyAllWindows()  # destroy all windows
