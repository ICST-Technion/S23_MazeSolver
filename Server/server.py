import socket
import threading
import time
import logging

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

def get_directions():
    return [1, 2, 3, 4, 5]


class DirectionsServer:
    def __init__(self):
        self.ip = Config.host
        self.port = Config.port
        self.directions = get_directions()
        self.lock = threading.Lock()
        self.request_counter = 0

        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        logging.info("started new server instance")

    def get_next_direction(self):
        return self.directions.pop()

    def update_directions(self):
        logging.debug("updating directions")
        self.lock.acquire()
        self.directions = get_directions()
        # get directions logic
        time.sleep(4)

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
                        if not data:
                            break

                        self.request_counter += 1
                        # every 5 requests update directions
                        if self.request_counter % 5 == 0:
                            t = threading.Thread(target=self.update_directions)
                            t.start()

                        # if recalculating directions tell bot to stay
                        if self.lock.locked():
                            logging.debug("updating in progress")
                            next_direction = Config.stay
                        else: # get next direction
                            next_direction = self.get_next_direction()

                        # send data to bot and log to console
                        conn.sendall(next_direction.to_bytes(1, "little"))
                        logging.debug(f"sent direction: {Config.directions_map[next_direction]}")


if __name__ == "__main__":
    server = DirectionsServer()
    server.start_server()