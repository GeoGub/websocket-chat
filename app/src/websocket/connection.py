from fastapi import WebSocket

from src.message.schema import MessageInput

class ConnectionManager:
    def __init__(self) -> None:
        self.connections: list[WebSocket] = []

    async def connection(self, websocket: WebSocket):
        self.connections.append(websocket)
        await websocket.accept()

    async def broadcast(self, message: MessageInput):
        for connection in self.connections:
            await connection.send_text(message.message)
    
    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)


connection_manager = ConnectionManager()