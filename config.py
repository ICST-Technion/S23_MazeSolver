import cv2


class Config:
    # Server Configurations

    # host ip
    host = "192.168.5.1"  # RPI
    # port to serve control server on
    webserver_port = 7000
    # port to serve commands server on
    port = 8080

    # Movement Configurations

    # num pixels to move before sampling camera
    interval_size = 18
    # amount of time to rotate for
    rotation_interval_size = 12
    # minimum degree error in rotation
    rotation_sensitivity = 5
    # minimum number of consecutive actions for solver to consider a movement
    min_actions_for_movement = 10
    # minimum pixels for aruco to move to consider a movement
    moved_sensitivity = 30
    # number of pixels for car to be apart from its destination to consider as moved
    accuracy_threshold = 4
    # speed to pass to the car for rotations
    rotation_speed = 60
    # max speed in forward movement
    max_forward_speed = 200
    min_forward_speed = 65
    # max speeds for rotation
    max_rotation_speed = 70
    min_rotation_speed = 30
    # error that occurs from difference in motors
    natural_error = 0
    # number of pixels for the car to be apart from its destination to consider as finished
    accuracy_threshold_for_complete = 60

    # PID params

    kp = 1.5
    ki = .1
    kd = 2

    # angle PID params
    a_kp = 3
    a_ki = .1
    a_kd = 2

    # Directions Protocol Configurations

    # value associated with direction
    right = 1
    left = 2
    up = 3
    down = 4
    stay = 5
    finished = 6
    # dict mapping names to values
    actions_to_num = {"UP": 3, "DOWN": 4, "LEFT": 2, "RIGHT": 1,
                      "DIAG_UL": 5, "DIAG_UR": 5, "DIAG_DL": 5, "DIAG_DR": 5, "STAY": 5}
    action_vectors = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1),
       "DIAG_UL": (-1, -1), "DIAG_UR": (-1, 1), "DIAG_DL": (1, -1), "DIAG_DR": (1, 1)}
    # opcodes according to communication protocol
    opcodes = {
        "DIRECTION_REQUEST": 1,
        "DIRECTION_MSG": 2,
        "ESP32_ACK": 3,
        "Control": 4
    }
    # device codes according to communication protocol
    dev_codes = {
        "RPI": 31,
        "ESP_32": 32,
        "Controller": 33
    }

    # logging file
    logging_file = "./maze_solver.log"

    # Image Processing Configurations

    # aruco dictionary used
    aruco_dict = cv2.aruco.DICT_4X4_100
    # location to retrieve image from if flag for from file is used (only for testing)
    image_file = "./saved.jpg"
    # resolution of images
    camera_resolution = (2592, 1936)
    # frame rate
    frame_rate = 12
    # width of actual maze, allows for better perspective transformation
    maze_width = 1189
    # height of actual maze, allows for better perspective transformation
    maze_height = 849
    line_width = 4
    # ID to use for the car, should not be an id used by any of the aruCos
    CAR_ID = 4
    # the aruCo ID used for the back of the car
    BACKWARD_CAR_ID = 3
    # the aruCo ID used for the front of the car
    FORWARD_CAR_ID = 1
    # the aruCo ID used for the end
    END_ID = 0

