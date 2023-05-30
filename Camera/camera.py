from config import Config
from ImageProcessing.preprocess_maze import MazeImage
from ImageProcessing.search_env import MazeSearchEnv
from ImageProcessing.search_agents import Heuristic1, WeightedAStarAgent, ContextHeuristic
from Server.server import DirectionsServer
import logging
import subprocess
import threading
from distance_calibration.confidence_based import PIDController, ConfidenceCalibrator
from picamera import PiCamera
from time import sleep
import numpy as np


class Camera:
    def __init__(self, frame_rate=4, camera_resolution=(1000, 1000)):
        self._image = np.empty((camera_resolution[1], camera_resolution[0]), dtype=np.uint8)
        self.picture_lock = threading.Lock()
        self.is_capturing = False
        self.frame_rate = frame_rate
        self.cam = PiCamera()
        self.cam.resolution = camera_resolution


    def retrieve_image(self):
        self.picture_lock.acquire(blocking=True)
        im = self._image.copy()
        self.picture_lock.release()
        return im

    def take_image(self):
        self.picture_lock.acquire(blocking=True)
        self.cam.capture(self._image, 'gray')
        self.picture_lock.release()

    def live_capture(self):
        while self.is_capturing:
            # Camera warm-up time
            self.picture_lock.acquire(blocking=True)
            self.cam.capture(self._image, 'gray')
            self.picture_lock.release()
            sleep(1 / self.frame_rate)

    def start_live_capture(self):
        self.is_capturing = True
        t = threading.Thread(target=self.live_capture)
        t.start()

    def stop_live_capture(self):
        self.is_capturing = False
