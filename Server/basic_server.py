import asyncio
import websockets
import threading
import time
import json
import cv2
import base64
from PIL import Image
from io import BytesIO
import numpy as np

set_as = False
MESSAGE = ""
async def handle_client(websocket, path):
    # Handle incoming messages from the client
    async for message in websocket:
        global set_as
        print(f"Received message: {message}")
        if message == "start":
            print("start")
            set_as = True
        if message == "stop":
            print("stop")
            set_as = False
        if message == "reset":
            print("reset")

        if message == "pic":
            print("reset")
            im = cv2.imread("../Camera/problem_pics/test-3.jpg")
            success, binary_data = cv2.imencode('.jpg', im)

            base64_data = base64.b64encode(binary_data).decode('utf-8')

            status = {"type": "maze", "maze": base64_data}
            await websocket.send(json.dumps(status))

        if message == "status":
            status = {"type": "status", "status": {
                "connection": True,
                "path_found": False,
                "running": set_as,
                "calculating_path": False,
            }}
            await websocket.send(json.dumps(status))

async def start_server():
    async with websockets.serve(handle_client, '192.168.1.18', 7000):  # Replace with your desired server IP and port
        print("WebSocket server started")
        await asyncio.Future()  # Run indefinitely

def run_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server())

run_server()