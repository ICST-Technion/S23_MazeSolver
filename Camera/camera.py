import threading
from picamera import PiCamera
import numpy as np
import cv2


"""
consider using

# Create a VideoCapture object for the Raspberry Pi camera
camera = cv2.VideoCapture(0)  # 0 for the first camera device

# Set the camera resolution (optional)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    ret, frame = camera.read()

"""

class Camera:
    def __init__(self, camera_resolution=(2592, 1936)):
        self.cam = PiCamera()
        self.cam.resolution = camera_resolution
        self._image = np.empty((self.cam.resolution[1], self.cam.resolution[0]), dtype=np.uint8)
        self._bgr_image = np.empty((self.cam.resolution[1]*self.cam.resolution[0]*3, ), dtype=np.uint8)
        self.picture_lock = threading.Lock()
        self.is_capturing = False


    def retrieve_image(self):
        self.picture_lock.acquire(blocking=True)
        im = self._image.copy()
        self.picture_lock.release()
        return im

    def take_image(self):
        self.picture_lock.acquire(blocking=True)
        self.cam.capture(self._bgr_image, 'bgr')
        self._image = cv2.cvtColor(self._bgr_image.reshape(
            (self.cam.resolution[1], self.cam.resolution[0], 3)),
                                   cv2.COLOR_BGR2GRAY)
        self.picture_lock.release()

    def live_capture(self):
        while self.is_capturing:
            self.picture_lock.acquire(blocking=True)
            self.cam.capture(self._bgr_image, 'bgr')
            self._image = cv2.cvtColor(self._bgr_image.reshape(
            (self.cam.resolution[1], self.cam.resolution[0], 3)),
                                   cv2.COLOR_BGR2GRAY)
            self.picture_lock.release()

    def save_image(self, name):
        cv2.imwrite(name, self._bgr_image.reshape(
            (self.cam.resolution[1], self.cam.resolution[0], 3)))
        cv2.imwrite("gray_" + name, self._image)

    def start_live_capture(self):
        self.is_capturing = True
        t = threading.Thread(target=self.live_capture)
        t.start()

    def stop_live_capture(self):
        self.is_capturing = False
