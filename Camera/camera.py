import threading
from picamera import PiCamera
import numpy as np
import cv2


"""
Camera module

provides basic interface with the raspberry pi camera that fits the better the requirements of the project
"""

class Camera:
    def __init__(self, camera_resolution=(2592, 1936)):
        # initialize camera configurations
        self.cam = PiCamera()
        self.cam.resolution = camera_resolution
        # variable that holds the current grayscale image
        self._image = np.empty((self.cam.resolution[1], self.cam.resolution[0]), dtype=np.uint8)
        # variables that holds the current BGR image
        self._bgr_image = np.empty((self.cam.resolution[1]*self.cam.resolution[0]*3, ), dtype=np.uint8)
        # a lock to prevent writing to the image variable and reading at the same time
        self.picture_lock = threading.Lock()
        # flag that indicates whether camera is capturing pictures
        self.is_capturing = False

    def retrieve_image(self):
        """
        retrieves the current image in a threading safe manenr
        :return: numpy array that holds image
        """
        self.picture_lock.acquire(blocking=True)
        im = self._image.copy()
        self.picture_lock.release()
        return im

    def take_image(self):
        """
        takes a single image in a threading safe manner
        :return: numpy array that contains image
        """
        self.picture_lock.acquire(blocking=True)
        self.cam.capture(self._bgr_image, 'bgr')
        self._image = cv2.cvtColor(self._bgr_image.reshape(
            (self.cam.resolution[1], self.cam.resolution[0], 3)),
                                   cv2.COLOR_BGR2GRAY)
        self.picture_lock.release()

    def live_capture(self):
        """
        Starts live capture of camera feed in a threading safe manner in a blocking manner
        :return: None
        """
        while self.is_capturing:
            self.picture_lock.acquire(blocking=True)
            self.cam.capture(self._bgr_image, 'bgr')
            self._image = cv2.cvtColor(self._bgr_image.reshape(
            (self.cam.resolution[1], self.cam.resolution[0], 3)),
                                   cv2.COLOR_BGR2GRAY)
            self.picture_lock.release()

    def save_image(self, name):
        """
        saves image to disk
        :param name: path to file to save to
        :return: None
        """
        cv2.imwrite(name, self._bgr_image.reshape(
            (self.cam.resolution[1], self.cam.resolution[0], 3)))
        cv2.imwrite("gray_" + name, self._image)

    def start_live_capture(self):
        """
        initializes a live capture in a non-blocking manner
        :return: None
        """
        self.is_capturing = True
        t = threading.Thread(target=self.live_capture)
        t.start()

    def stop_live_capture(self):
        """
        stops any live capture currently occurring
        :return: None
        """
        self.is_capturing = False
