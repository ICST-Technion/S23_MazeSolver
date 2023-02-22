#!/usr/bin/env python
# coding: utf-8

# In[15]:


import cv2
import numpy as np
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[16]:


def show_image(img):
    plt.imshow(img)
    plt.show()


# In[46]:


# loads image from path
# returns numpy array
def load_raw_image(path):
    # Load using opencv
    raw_image = cv2.imread(path)
    # convert your lists into a numpy array of size (N, C, H, W)
    return np.array(raw_image)


# In[30]:


def threshold_image(img, min_val=127, max_val = 255):
    ret,thresh = cv2.threshold(img,min_val, max_val,cv2.THRESH_BINARY)
    return thresh


# In[44]:


def get_start_point(img):
    return im.shape[0]-1, 0


# In[45]:


def get_end_point(img):
    return 0, im.shape[1]-1


# In[47]:


def load_image(path):
    im = load_raw_image("./practice_maze.png")
    im = threshold_image(im)
    return im


# In[ ]:




