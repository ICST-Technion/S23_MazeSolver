#!/usr/bin/env python
# coding: utf-8

# In[14]:


import cv2
import numpy as np
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[15]:


MAZE_COLOR = 255
BACKGROUND_COLOR = 0


# In[72]:


def show_image(img):
    plt.imshow(img, cmap='gray')
    plt.show()


# In[17]:


# loads image from path
# returns numpy array
def load_raw_image(path):
    # Load using opencv
    raw_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # convert your lists into a numpy array of size (N, C, H, W)
    return np.array(raw_image)


# In[34]:


def threshold_image(img, min_val=127, max_val = 255):
    ret,thresh = cv2.threshold(img,min_val, max_val,cv2.THRESH_BINARY_INV)
    return thresh


# In[44]:


def get_start_point(img):
    positions = np.nonzero(img)
    start_idx = np.argmin(positions[0])

    return positions[0][start_idx], positions[1][start_idx]


# In[71]:


def get_end_point(img):
    positions = np.nonzero(img)
    start_idx = np.argmax(positions[0])

    return positions[0][start_idx], positions[1][start_idx]


# In[46]:


def load_image(path):
    im = load_raw_image("./practice_maze.png")
    im = threshold_image(im)
    return im


# In[47]:


class MazeImage(object):
    def __init__(self, path):
        self.data = load_image(path)
        self.__endpoint = get_end_point(self.data)
        self.__startpoint = get_start_point(self.data)
    
    def is_on_maze(self, row, col):
        return self.data[row][col] == MAZE_COLOR
    
    def get_max_row(self):
        return self.data.shape[0]
    
    def get_max_col(self):
        return self.data.shape[1]
    
    def get_data(self):
        return self.data
    
    def get_end_point(self):
        # consider making not precise point
        return self.__endpoint
    
    def get_start_point(self):
        return self.__startpoint


# In[ ]:




