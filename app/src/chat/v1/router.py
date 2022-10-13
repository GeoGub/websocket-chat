from fastapi import APIRouter, Depends, Response

from src.auth.security import get_current_user
from src.sample_schemas import Params
from src.chat.schema import ChatListSchema, ChatSchema
from src.crud.crud_chat import crud_chat
from src.user.schema import UserSchema


chat_router = APIRouter(prefix="/chats")


@chat_router.get("/", response_model=ChatListSchema)
async def get_chats(params: Params = Depends(), current_user: UserSchema = Depends(get_current_user)):
    chats, total = await crud_chat.read(params.dict(), current_user)
    print(chats)
    chats = [ChatSchema(
        user_iniciator=UserSchema(username=chat.username, id=chat.id_1),
        user=UserSchema(username=chat.username_1, id=chat.id_2),
        **{**chat}
    ) for chat in chats]
    print(len(chats))
    response = ChatListSchema(items=chats, total=total, **params.dict())
    return response
