#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import preprocess_maze


# In[15]:


from preprocess_maze import MazeImage, show_image


# In[27]:


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
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


class MazeSearchEnv(object):
    
    # data object must contain
    # is_at_end
    # get_start_point
    # get_data
    def __init__(self, path_to_maze):
        self.actions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
        self.__data_obj = MazeImage(path_to_maze)
        end_row, end_col = self.__data_obj.get_end_point()
        self.__final_state = MazeState(end_row, end_col)
        
    def is_final_state(self, state):
        return state == self.__final_state
    
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
    
    def print_maze(self):
        show_image(self.__data_obj.get_data())


# In[ ]:




