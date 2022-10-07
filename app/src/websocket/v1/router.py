from fastapi import APIRouter, WebSocket, Depends

import json

from src.database import database
from src.websocket.connection import connection_manager
from src.message.schema import MessageInput
from src.crud.crud_message import crud_message
from src.user.schema import UserSchema

websocket_router = APIRouter(prefix="/websocket")

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connection(websocket=websocket)
    while True:
        try:
            data = await websocket.receive_text()
        except Exception as e:
           await connection_manager.disconnect(websocket)
           return None
        _, data = await crud_message.create(database, MessageInput(**json.loads(data)))
        await connection_manager.broadcast(data)