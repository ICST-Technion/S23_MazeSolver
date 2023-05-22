import asyncio
import websockets
import threading
import time

MESSAGE = ""
async def handle_client(websocket, path):
    # Handle incoming messages from the client
    async for message in websocket:
        print(f"Received message: {message}")
        if message == "start":
            print("start")
        if message == "stop":
            print("stop")
        if message == "reset":
            print("reset")

async def start_server():
    async with websockets.serve(handle_client, '192.168.1.101', 8080):  # Replace with your desired server IP and port
        print("WebSocket server started")
        await asyncio.Future()  # Run indefinitely

def run_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server())


server_thread = threading.Thread(target=run_server)
server_thread.start()

while True:
    time.sleep(5)