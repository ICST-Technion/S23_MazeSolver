import socket
import threading
import time
import logging
import asyncio
import websockets
import math

from config import Config


def dist(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 +
              (c1[1] - c2[1]) ** 2)

class DirectionsServer:
    def __init__(self, ip, port, maze):
        self.stopped = True
        self.ip = ip
        self.port = port
        self.lock = threading.Lock()
        self.maze = maze
        logging.basicConfig(filename=Config.logging_file, level=logging.DEBUG)
        logging.info("started new server instance")


    def updating_started(self):
        self.lock.acquire()

    def finished_updating(self):
        self.lock.release()

    def parse_message(self, data):
        opcode = data[0:1]
        src_dev = data[1:2]
        dst_dev = data[2:3]
        direction = data[3:4]
        l = data[4:8]
        r = data[8:12]
        time = data[12:16]

        return {"opcode": int.from_bytes(opcode, byteorder="little"),
                "src_dev": int.from_bytes(src_dev, byteorder="little"),
                "dst_dev": int.from_bytes(dst_dev, byteorder="little"),
                "direction": int.from_bytes(direction, byteorder="little"),
                "time": int.from_bytes(time, byteorder="little"),
                "left_speed": int.from_bytes(l, byteorder="little"),
                "right_speed": int.from_bytes(r, byteorder="little")
                }

    def create_message(self, opcode, src, dst, dir, l, r, time):
        msg = opcode.to_bytes(1, "little") + src.to_bytes(1, "little") + dst.to_bytes(1, "little")\
              + dir.to_bytes(1, "little") \
              + l.to_bytes(4, "little") + r.to_bytes(4, "little") + time.to_bytes(4, "little")
        return msg

    def start_server(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5000)
            # start up server
            try:
                s.bind((self.ip, self.port))
                s.listen()
            except Exception as e:
                logging.error(f"Server startup error: {repr(e)}")

            while True:
                logging.debug(f"Server Listening")
                conn, addr = s.accept()
                with conn:
                    logging.debug(f"Connected by {addr}")
                    while True:
                        # receive data from bot
                        data = conn.recv(1024)
                        parsed_message = self.parse_message(data)

                        if not data or parsed_message['opcode'] not in list(Config.opcodes.values()):
                            continue

                        if parsed_message['opcode'] == Config.opcodes['DIRECTION_REQUEST']:
                            if self.stopped:
                                logging.debug("server stopped")
                                next_direction = (Config.stay, 0, 0, 0)
                            else:
                                # recalculate coefficient and confidence from last movement
                                self.maze.update_step()
                                if self.lock.locked():
                                    logging.debug("updating in progress")
                                    next_direction = (Config.stay, 0, 0, 0)
                                else:  # get next direction
                                    next_direction = self.maze.get_next_direction()

                            msg = self.create_message(Config.opcodes['DIRECTION_MSG'],
                                                      Config.dev_codes['RPI'],
                                                      Config.dev_codes['ESP_32'],
                                                      next_direction[0],
                                                      next_direction[1],
                                                      next_direction[2],
                                                      next_direction[3]
                                                      )
                            # send data to bot and log to console
                            conn.sendall(msg)
                            print(next_direction)
                            logging.debug(f"sent direction: {Config.directions_map[next_direction[0]]}"
                                          f" ,{next_direction[1]}, {next_direction[2], next_direction[3]}")
                            data = conn.recv(1024)
                            parsed_message = self.parse_message(data)
                            if parsed_message['opcode'] == Config.opcodes['ESP32_ACK']:
                                logging.debug(f"Received ACK")

    async def handle_client(self, websocket, path):
        # Handle incoming messages from the client
        async for message in websocket:
            print(f"Received message: {message}")
            if message == "start":
                self.stopped = False
            if message == "stop":
                self.stopped = True
            if message == "reset":
                self.request_counter = 0
                self.maze.update_directions()


    async def start_webserver(self):
        async with websockets.serve(self.handle_client, Config.host, Config.webserver_port):
            print("WebSocket server started")
            await asyncio.Future()  # Run indefinitely

    def run_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_webserver())

if __name__ == "__main__":
    pass
