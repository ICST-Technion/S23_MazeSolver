from picamera import PiCamera
from time import sleep
import os


def camera_test():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    path = '/home/pi/Desktop/MazeSolver/Camera/test.jpg'
    camera.capture(path)
    camera.stop_preview()
    if os.path.exists(path):
        print("Test: passed")
    else:
        print("Test: failed")


def aruco_test():
    pass



if __name__ == "__main__":
    camera_test()