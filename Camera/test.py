from picamera import PiCamera
from time import sleep
import os

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

#os.remove(path)



