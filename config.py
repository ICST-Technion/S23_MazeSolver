import cv2


class Config:
    # server socket
    # host = "127.0.0.1"  # PC
    host = "192.168.5.1"  # RPI
    webserver_port = 7000
    port = 8080

    # Tuning
    learning_rate = 0.001
    lower_confidence_thresh = 0.8
    error_update_thresh = 0.05  # 0 - 1
    interval_size = 50
    right_angle = 680


    # PID params
    kp = 2
    ki = .25
    kd = 0.5
    # angle PID params
    a_kp = 3.2
    a_ki = .1
    a_kd = 3

    # bot
    right = 1
    left = 2
    up = 3
    down = 4
    stay = 5
    finished = 6
    directions_map = {1: "RIGHT", 2: "LEFT", 3: "UP", 4: "DOWN", 5: "STAY", 6: "FINISHED"}
    actions_to_num = {"UP": 3, "DOWN": 4, "LEFT": 2, "RIGHT": 1,
                      "DIAG_UL": 5, "DIAG_UR": 5, "DIAG_DL": 5, "DIAG_DR": 5, "STAY": 5}
    angle_map = {"LEFT": 270, "UP": 0, "DOWN": 180, "RIGHT": 90}
    rotation_sensitivity = 2
    min_actions_for_movement = 10

    opcodes = {
        "DIRECTION_REQUEST": 1,
        "DIRECTION_MSG": 2,
        "ESP32_ACK": 3,
        "Control": 4
    }

    dev_codes = {
        "RPI": 31,
        "ESP_32": 32,
        "Controller": 33
    }

    # logging
    logging_file = "./maze_solver.log"

    # Image processing
    aruco_dict = cv2.aruco.DICT_4X4_100
    image_file = "./saved.jpg"
    camera_resolution = (2592, 1936)
    frame_rate = 6
    maze_width = 1189
    maze_height = 849
    # image_file = "./Camera/sample_images/good2.jpg"
    CAR_ID = 4
    BACKWARD_CAR_ID = 3
    FORWARD_CAR_ID = 1
    END_ID = 0

    moved_sensitivity = 30
    accuracy_threshold = 15

    rotation_speed = 100

