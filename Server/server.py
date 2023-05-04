import socket
import threading
import time
import logging

from config import Config


class DirectionsServer:
    def __init__(self, ip, port, maze):
        self.ip = ip
        self.port = port
        self.directions = []
        self.lock = threading.Lock()
        self.request_counter = 0
        self.maze = maze
        self.update_directions()
        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        logging.info("started new server instance")

    def get_next_direction(self):
        action = self.directions[0][0]
        angle = self.maze.get_car_angle()
        if (abs(angle - Config.angle_map[action])) > Config.rotation_sensitivity:
            diff = angle - Config.angle_map[action]
            rotate_dir = "LEFT" if diff < 0 else "RIGHT"
            return Config.actions_to_num[rotate_dir], int(abs(diff))
        direction = self.directions.pop(0)
        return Config.actions_to_num["UP"], int(direction[1])

    def update_directions(self):
        logging.debug("updating directions")
        self.lock.acquire()
        self.directions = self.maze.update()
        # get directions logic
        time.sleep(1)
        self.lock.release()

    def parse_message(self, data):
        opcode = data[0:1]
        src_dev = data[1:2]
        dst_dev = data[2:3]
        direction = data[3:4]
        msg_data = data[4:8]
        return {"opcode": int.from_bytes(opcode, byteorder="little"),
                "src_dev": int.from_bytes(src_dev, byteorder="little"),
                "dst_dev": int.from_bytes(dst_dev, byteorder="little"),
                "direction": int.from_bytes(direction, byteorder="little"),
                "data": int.from_bytes(msg_data, byteorder="little")
                }

    def create_message(self, opcode, src, dst, dir, data):
        msg = opcode.to_bytes(1, "little") + src.to_bytes(1, "little") + dst.to_bytes(1, "little")\
              + dir.to_bytes(1, "little") + data.to_bytes(4, "little")
        return msg

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5000)
            # start up server
            try:
                s.bind((self.ip, self.port))
                s.listen()
            except Exception as e:
                logging.error(f"Server startup error: {repr(e)}")

            while True:
                conn, addr = s.accept()
                with conn:
                    logging.debug(f"Connected by {addr}")
                    while True:
                        # receive data from bot
                        data = conn.recv(1024)
                        parsed_message = self.parse_message(data.decode())

                        esp_req = data.decode().split(':')[0]
                        if not data or parsed_message['opcode'] not in list(Config.opcodes.values()):
                            continue
                        if parsed_message['opcode'] == Config.opcodes['DIRECTION_REQUEST']:
                            self.request_counter += 1
                            # every 5 requests update directions
                            # if self.request_counter % 5 == 0:
                            #     t = threading.Thread(target=self.update_directions)
                            #     t.start()
                            # if recalculating directions tell bot to stay
                            if self.lock.locked():
                                logging.debug("updating in progress")
                                next_direction = (Config.stay, 0)
                            else:  # get next direction
                                next_direction = self.get_next_direction()

                            msg = self.create_message(Config.opcodes['DIRECTION_MSG'],
                                                      Config.dev_codes['RPI'],
                                                      Config.dev_codes['ESP_32'],
                                                      next_direction[0],
                                                      next_direction[1]
                                                      )
                            # send data to bot and log to console
                            conn.sendall(msg)
                            logging.debug(f"sent direction: {Config.directions_map[next_direction[0]]}"
                                          f" ,{next_direction[1]}")
                            data = conn.recv(1024)
                            parsed_message = self.parse_message(data)
                            if parsed_message['opcode'] == Config.opcodes['ESP32_ACK']:
                                logging.debug(f"Received ACK")


if __name__ == "__main__":
    pass
