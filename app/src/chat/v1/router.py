from fastapi import APIRouter, Depends, Response

from src.auth.security import get_current_user
from src.sample_schemas import Params
from src.chat.schema import ChatListSchema
from src.crud.crud_chat import crud_chat


chat_router = APIRouter(prefix="/chats")

chat_router.get("/", response_model=ChatListSchema)
async def get_chats(params: Params = Depends()):
    chats, total = await crud_chat.read(params)
