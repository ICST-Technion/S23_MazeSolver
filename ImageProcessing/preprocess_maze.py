#!/usr/bin/env python
# coding: utf-8

# In[25]:


import cv2
import math
import numpy as np
from skimage.morphology import skeletonize

from config import Config
# In[26]:

r = 0
MAZE_COLOR = 255
BACKGROUND_COLOR = 0
origin = [2, 3]
refvec = [0, 1]

# In[27]:

# In[28]:


# loads image from path
# returns numpy array
def load_raw_image(path):
    # Load using opencv
    raw_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # convert your lists into a numpy array of size (N, C, H, W)
    return np.array(raw_image)



def clockwiseangle_and_distance(point):
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector

def cyclic_intersection_pts(pts):
    """
    Sorts 4 points in clockwise direction with the first point been closest to 0,0
    Assumption:
        There are exactly 4 points in the input and
        from a rectangle which is not very distorted
    """
    if pts.shape[0] != 4:
        return None

    # Calculate the center
    center = np.mean(pts, axis=0)

    # Sort the points in clockwise
    cyclic_pts = [
        # Top-left
        pts[np.where(np.logical_and(pts[:, 0] < center[0], pts[:, 1] < center[1]))[0][0], :],
        # Top-right
        pts[np.where(np.logical_and(pts[:, 0] > center[0], pts[:, 1] < center[1]))[0][0], :],
        # Bottom-Right
        pts[np.where(np.logical_and(pts[:, 0] > center[0], pts[:, 1] > center[1]))[0][0], :],
        # Bottom-Left
        pts[np.where(np.logical_and(pts[:, 0] < center[0], pts[:, 1] > center[1]))[0][0], :]
    ]

    return np.array(cyclic_pts)


def point_on_image(x: int, y: int, image_shape: tuple):
    """
    Returns true is x and y are on the image
    """
    return 0 <= y < image_shape[0] and 0 <= x < image_shape[1]



def angle_to(point):
  return math.atan2(point[1], point[0])


def warp_image(img, thresh, buffer=50):
    edges = cv2.Canny(thresh, 100, 200, apertureSize=7)
    # Save the edge detected image
    cv2.imwrite('edges.jpg', edges)
    # find edges
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    # Fit a rotated rect
    rotatedRect = cv2.minAreaRect(largest_contour)
    corners = cv2.goodFeaturesToTrack(edges, 4, 0.1, 500)
    corners = corners.reshape(corners.shape[0], 2).astype(np.int32)
    corners = cyclic_intersection_pts(corners)
    # Get rotated rect dimensions
    (x, y), (width, height), angle = rotatedRect
    width = 849 # img.shape[1]
    height = 1189 # img.shape[0]
    dstPts = [[0, 0], [width, 0], [width, height], [0, height]]
    corners[0] -= buffer
    corners[1] = [corners[1][0] + buffer, corners[1][1] - buffer]
    corners[2] += buffer
    corners[3] = [corners[3][0] - buffer, corners[3][1] + buffer]
    # Get the transform
    m = cv2.getPerspectiveTransform(np.float32(corners), np.float32(dstPts))
    # Transform the image
    out = cv2.warpPerspective(img, m, (int(width), int(height)))
    # Save the output
    return out

def straighten_image(img, contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box).astype(np.float32)
    # if the object is planar
    target_points = np.array([[0, 0],
                              [img.shape[1], 0],
                              [img.shape[1], img.shape[0]],
                              [0, img.shape[0]]
                              ], dtype=np.float32)
    M = cv2.getPerspectiveTransform(box, target_points)
    # if the object is planar
    img_fixed = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))

    # if the object is not planar
    # img_fixed = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
    cv2.imwrite('fixed_image.jpg', img_fixed)

# In[29]:
def threshold_image(img, min_val=127, rotation=0, max_val=255):
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    thresh_cp = np.copy(thresh)
    thresh[thresh_cp == 255] = 0
    thresh[thresh_cp == 0] = 255
    # use morphology to remove the thin lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # find contours
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Contour of maximum area
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a mask from the largest contour
    mask = np.zeros_like(closed)
    cv2.drawContours(mask, [largest_contour], 0, 255, -1)
    thresh[mask == 0] = 255
    cv2.imwrite('./mask.png', mask)
    thresh_cp = np.copy(thresh)
    thresh[thresh_cp == 255] = 0
    thresh[thresh_cp == 0] = 255
    return thresh, mask


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


def fill_aruco(image, corners, extra=10):

    minc = min(corners, key=lambda x: x[0] + x[1])
    maxc = max(corners, key=lambda x: x[0] + x[1])
    return cv2.rectangle(image, ((int)(minc[0]) - extra, (int)(minc[1]) - extra) ,
                         ((int)(maxc[0]) + extra, (int)(maxc[1]) + extra) , 255, -1)


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
    max_i = 0
    max_val = 0
    for i in np.arange(-10, 10, 1):
        num_lines = get_num_lines(i, edges)
        if num_lines > max_val:
            max_val = num_lines
            max_i = i
    return max_i



def load_image_post_aruco(im, rotation, thresh_val=100):
    thresh, mask = threshold_image(im, min_val=thresh_val, rotation=rotation)
    skel = skeletonize_image(thresh).astype(np.uint8)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(skel, kernel, iterations=1)
    warped = warp_image(dilation, mask)
    warped_original = warp_image(im, mask)
    cv2.imwrite('warped.jpg', warped_original)
    return warped, warped_original

class ArucoData(object):
    def __init__(self, img, aruco_dict):
        # car ID : 1
        self.aruco_dict = aruco_dict
        self.aruco_info = {}
        self.extract_basic_info(img)

    def extract_basic_info(self, img):

        dictionary = cv2.aruco.getPredefinedDictionary(self.aruco_dict)
        parameters = cv2.aruco.DetectorParameters()  # PC
        parameters.useAruco3Detection = True
        detector = cv2.aruco.ArucoDetector(dictionary, parameters)  # PC
        # markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(img, dictionary)  # RPI
        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(img) # PC
        # Detect the ArUco markers in the image
        print(markerIds)
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
        # data = rotate_image(data, self.rotation)
        self.data, warped_orig = load_image_post_aruco(data, self.rotation)
        self.__endpoint = (150, 1102)
        self.__startpoint = get_start_point(self.data)
        self.aruco = ArucoData(warped_orig, aruco_dict)
        fill_aruco(self.data, self.aruco.aruco_info[Config.CAR_ID]['corners'])
        fill_aruco(self.data, self.aruco.aruco_info[Config.END_ID]['corners'])
        print('here',self.aruco.aruco_info[Config.CAR_ID]['rotation'])
        print('here',self.aruco.aruco_info[Config.END_ID]['rotation'])

        # fill_aruco(self.data, self.aruco.aruco_info[Config.END_ID]['corners'])
        cv2.imwrite('./example.jpg', self.data)

    def load_image(self, path):
        data = load_raw_image(path)
        # data = rotate_image(data, self.rotation)
        self.data, warped_orig = load_image_post_aruco(data, self.rotation)
        self.__endpoint = (150, 1102)
        self.__startpoint = get_start_point(self.data)
        self.aruco = ArucoData(warped_orig, self.aruco_dict)
        fill_aruco(self.data, self.aruco.aruco_info[Config.CAR_ID]['corners'])
        fill_aruco(self.data, self.aruco.aruco_info[Config.END_ID]['corners'])

    def get_car_angle(self):
        return self.aruco.aruco_info[Config.CAR_ID]['rotation']

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
        # return self.__endpoint
        return self.aruco.aruco_info[Config.END_ID]['centerY'], self.aruco.aruco_info[Config.END_ID]['centerX']

    def get_start_point(self):
        return self.get_current_point()

    def get_current_point(self):
        return self.aruco.aruco_info[Config.CAR_ID]['centerY'], self.aruco.aruco_info[Config.CAR_ID]['centerX']
