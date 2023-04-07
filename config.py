import cv2

class Config:

    # server socket
    host = "127.0.0.1"  # should be 192.168.5.1 for RPI
    port = 8080

    # bot
    right = 1
    left = 2
    up = 3
    down = 4
    stay = 5
    finished = 6
    directions_map = {1: "RIGHT", 2: "LEFT", 3:"UP", 4:"down", 5:"STAY", 6:"FINISHED"}

    # logging
    logging_file = "./maze_solver.log"

    # Image processing
    aruco_dict = cv2.aruco.DICT_4X4_50
    image_file = "./Camera/sample_images/test-3.jpg"

