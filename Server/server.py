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
        action = self.directions[0]
        angle = self.maze.get_car_angle()
        if(abs(angle - Config.angle_map[action])) > Config.rotation_sensitivity:
            diff = angle - Config.angle_map[action]
            rotate_dir = "LEFT" if diff < 0 else "RIGHT"
            return Config.actions_to_num[rotate_dir], abs(diff)
        direction = self.directions.pop(0)
        return Config.actions_to_num[direction[0]], direction[1]

    def update_directions(self):
        logging.debug("updating directions")
        self.lock.acquire()
        self.directions = self.maze.update()
        # get directions logic
        time.sleep(1)
        self.lock.release()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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
                        if not data or data.decode() != 'dir:':
                            break

                        self.request_counter += 1
                        # every 5 requests update directions
                        if self.request_counter % 5 == 0:
                            t = threading.Thread(target=self.update_directions)
                            t.start()

                        # if recalculating directions tell bot to stay
                        if self.lock.locked():
                            logging.debug("updating in progress")
                            next_direction = (Config.stay, 0)
                        else: # get next direction
                            next_direction = self.get_next_direction()

                        # send data to bot and log to console
                        conn.sendall(next_direction[0].to_bytes(1, "little"))
                        conn.sendall(next_direction[1].to_bytes(2, "little"))
                        logging.debug(f"sent direction: {Config.directions_map[next_direction]}")


if __name__ == "__main__":
    pass