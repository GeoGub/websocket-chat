from fastapi import APIRouter, WebSocket

from src.database import database
from src.websocket.connection import connection_manager
from src.message.schema import MessageInput
from src.crud.crud_message import crud_message

websocket_router = APIRouter(prefix="/websocket")

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connection(websocket=websocket)
    while True:
        try:
            message = await websocket.receive_text()
        except Exception as e:
           await connection_manager.disconnect(websocket)
           return None
        message_input = MessageInput(message=message, sender_id=1)
        await crud_message.create(database, message_input)
        await connection_manager.broadcast(message_input)