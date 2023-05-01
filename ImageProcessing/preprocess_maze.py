#!/usr/bin/env python
# coding: utf-8

# In[25]:


import cv2
import numpy as np
from skimage.morphology import skeletonize

from config import Config
# In[26]:


MAZE_COLOR = 255
BACKGROUND_COLOR = 0


# In[27]:

# In[28]:


# loads image from path
# returns numpy array
def load_raw_image(path):
    # Load using opencv
    raw_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # convert your lists into a numpy array of size (N, C, H, W)
    return np.array(raw_image)


# In[29]:


def threshold_image(img, min_val=127, max_val=255):
    ret, thresh = cv2.threshold(img, min_val, max_val, cv2.THRESH_BINARY_INV)
    return thresh


def get_start_point(img):
    positions = np.nonzero(img)
    start_idx = np.argmin(positions[0])

    return positions[0][start_idx], positions[1][start_idx]


# In[31]:


def get_end_point(img):
    return 315, 406
    positions = np.nonzero(img)
    start_idx = np.argmax(positions[0])
    return positions[0][start_idx], positions[1][start_idx]


# In[32]:


def fill_aruco(image, corners):
    return cv2.rectangle(image, ((int)(corners[0][0]), (int)(corners[0][1])),
                         ((int)(corners[2][0]), (int)(corners[2][1])), 255, -1)


def skeletonize_image(image):
    image = np.copy(image)
    image[image != 0] = 1
    image = skeletonize(image).astype(int)
    image[image != 0] = MAZE_COLOR
    return image


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def get_num_lines(angle, edges):
    epsilon = .001
    angle = angle
    rotated_img = rotate_image(edges, angle)
    polar_lines = cv2.HoughLines(rotated_img, 1, np.pi / 180, 150, 0)
    angles = np.array(polar_lines[:, 0][:, 1])
    x = (((0 - epsilon <= angles) & (angles < 0 + epsilon)) |
            ((np.pi / 2 - epsilon <= angles) & (angles < np.pi + epsilon))).sum()
    return x


def get_rotation_to_straighten(image):
    edges = cv2.Canny(image, 10, 180, apertureSize=3)
    # Save the edge detected image
    cv2.imwrite('./edges.png', edges)
    max_i = 0
    max_val = 0
    for i in np.arange(-5, 5, .1):
        num_lines = get_num_lines(i, edges)
        if num_lines > max_val:
            max_val = num_lines
            max_i = i
    return max_i

def load_image_post_aruco(im, thresh_val=88):
    im = threshold_image(im, min_val=thresh_val)
    im = skeletonize_image(im).astype(np.uint8)
    return im

class ArucoData(object):
    def __init__(self, img, aruco_dict):
        # car ID : 1
        self.aruco_dict = aruco_dict
        self.aruco_info = {}
        self.extract_basic_info(img)

    def extract_basic_info(self, img):
        dictionary = cv2.aruco.getPredefinedDictionary(self.aruco_dict)
        parameters = cv2.aruco.DetectorParameters()  # remove for rpi
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)  # remove for rpi
        # change to cv2.aruco.detectMarkers for rpi
        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(img)
        for index, id in enumerate(markerIds):
            marker_corners = markerCorners[index][0]
            p1, p2 = marker_corners[0], marker_corners[1]
            angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0])) % 360
            self.aruco_info[id[0]] = {"corners": marker_corners,
                                   "centerX": int((marker_corners[0][0]
                                                   + marker_corners[1][0]
                                                   + marker_corners[2][0]
                                                   + marker_corners[3][0]) / 4),
                                   "centerY": int((marker_corners[0][1]
                                                   + marker_corners[1][1]
                                                   + marker_corners[2][1]
                                                   + marker_corners[3][1]) / 4),
                                   "rotation": float(angle),
                                   }

class MazeImage(object):
    def __init__(self, path, aruco_dict=cv2.aruco.DICT_4X4_50):
        data = load_raw_image(path)
        self.rotation = get_rotation_to_straighten(data)
        self.aruco_dict = aruco_dict
        data = rotate_image(data, self.rotation)
        self.data = load_image_post_aruco(data)
        self.__endpoint = get_end_point(self.data)
        self.__startpoint = get_start_point(self.data)
        self.aruco = ArucoData(data, aruco_dict)
        fill_aruco(self.data, self.aruco.aruco_info[Config.CAR_ID]['corners'])


    def load_image(self, path):
        data = load_raw_image(path)
        data = rotate_image(data, self.rotation)
        self.data = load_image_post_aruco(data)
        self.__endpoint = get_end_point(self.data)
        self.__startpoint = get_start_point(self.data)
        self.aruco = ArucoData(data, self.aruco_dict)
        fill_aruco(self.data, self.aruco.aruco_info[1]['corners'])

    def get_car_angle(self):
        return self.aruco.aruco_info[Config.CAR_ID]

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
        return self.get_current_point()

    def get_current_point(self):
        return self.aruco.aruco_info[Config.CAR_ID]['centerY'], self.aruco.aruco_info[Config.CAR_ID]['centerX']
