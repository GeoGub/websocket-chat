import asyncio
import websockets 
from websockets.legacy.server import WebSocketServer

async def echo(websocket:WebSocketServer):
    async for message in websocket:
        print(f"<<< message: {message}")
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
