import cv2


class Config:
    # server socket
    # host = "127.0.0.1"  # PC
    host = "192.168.5.1"  # RPI

    port = 8080

    # bot
    right = 1
    left = 2
    up = 3
    down = 4
    stay = 5
    finished = 6
    directions_map = {1: "RIGHT", 2: "LEFT", 3: "UP", 4: "down", 5: "STAY", 6: "FINISHED"}
    actions_to_num = {"UP": 3, "DOWN": 4, "LEFT": 2, "RIGHT": 1,
                      "DIAG_UL": 5, "DIAG_UR": 5, "DIAG_DL": 5, "DIAG_DR": 5}
    angle_map = {"LEFT": 180, "UP": 90, "DOWN": 270, "RIGHT": 0}
    rotation_sensitivity = 4
    min_actions_for_movement = 15

    opcodes = {
        "DIRECTION_REQUEST": 1,
        "DIRECTION_MSG": 2,
        "ESP32_ACK": 3,
    }

    dev_codes = {
        "RPI": 31,
        "ESP_32": 32
    }

    # logging
    logging_file = "./maze_solver.log"

    # Image processing
    aruco_dict = cv2.aruco.DICT_4X4_50
    image_file = "./Camera/sample_images/good2.jpg"
    CAR_ID = 1
    END_ID = 0

