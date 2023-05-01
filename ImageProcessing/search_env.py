#!/usr/bin/env python
# coding: utf-8

# In[32]:


import cv2
import numpy as np

from ImageProcessing.preprocess_maze import MazeImage

"""
includes:
    - States
    - operators
    - end state
    - initial state
"""


class MazeState(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def get_value(self):
        return self.row, self.col

    def get_id(self):
        return str(self.row) + "," + str(self.col)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __gt__(self, other):
        if self.row > other.row:
            return True
        elif self.row == other.row and self.col > other.col:
            return True
        return False

    def __lt__(self, other):
        if self.row < other.row:
            return True
        elif self.row == other.row and self.col < other.col:
            return True
        return False


class MazeSearchEnv(object):

    # data object must contain
    # is_at_end
    # get_start_point
    # get_data
    def __init__(self, path_to_maze, aruco_dict):
        self.actions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1),
                        "DIAG_UL": (-1, -1), "DIAG_UR": (-1, 1), "DIAG_DL": (1, -1), "DIAG_DR": (1, 1)}
        self.costs = {"UP": 1, "DOWN": 1, "LEFT": 1, "RIGHT": 1,
                        "DIAG_UL": 10, "DIAG_UR": 10, "DIAG_DL": 10, "DIAG_DR": 10}
        self.__data_obj = MazeImage(path_to_maze, aruco_dict)
        self.data = self.__data_obj
        end_row, end_col = self.__data_obj.get_end_point()
        self.__final_state = MazeState(end_row, end_col)
        self.__cost = 1


    def get_car_angle(self):
        return self.__data_obj.get_car_angle()

    def load_image(self, path):
        self.__data_obj.load_image(path)

    def get_cost(self, state, action):
        return self.costs[action]
        return self.__cost

    def is_final_state(self, state):
        return state == self.__final_state

    def get_final_state(self):
        return self.__final_state

    def get_initial_state(self):
        start_row, start_col = self.__data_obj.get_start_point()
        return MazeState(start_row, start_col)

    def is_legal_state(self, row, col):
        if row < 0 or row >= self.__data_obj.get_max_row():
            return False

        if col < 0 or col >= self.__data_obj.get_max_col():
            return False

        if not self.__data_obj.is_on_maze(row, col):
            return False

        return True

    def get_legal_operators(self, state):
        legal_actions = []
        curr_row, curr_col = state.get_value()
        for action_name, action in self.actions.items():
            new_row = curr_row + action[0]
            new_col = curr_col + action[1]
            if self.is_legal_state(new_row, new_col):
                legal_actions.append(action_name)
        return legal_actions

    def get_next_state(self, state, action):
        curr_row, curr_col = state.get_value()
        new_row = curr_row + self.actions[action][0]
        new_col = curr_col + self.actions[action][1]
        if not self.is_legal_state(new_row, new_col):
            raise RuntimeError("Illegal next state")
        return MazeState(new_row, new_col)

    def color_maze_path_and_print(self, actions, color=122):
        maze_copy = self.data.data.copy()
        curr_row, curr_col = self.get_initial_state().get_value()
        maze_copy[curr_row][curr_col] = color
        for action in actions:
            curr_row = curr_row + self.actions[action][0]
            curr_col = curr_col + self.actions[action][1]
            maze_copy[curr_row][curr_col] = color
        return maze_copy


# In[ ]:
