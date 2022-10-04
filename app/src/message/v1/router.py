from fastapi import APIRouter, Depends, Response, WebSocket

from src.database import database
from src.sample_schemas import Params, BadRequest
from src.auth.security import get_current_user
from src.message.schema import MessageInput, MessageListSchema
from src.user.schema import UserSchema
from src.crud.crud_message import crud_message


message_router = APIRouter(prefix='/messages')

@message_router.get('/', response_model=MessageListSchema)
async def get_messages(params: Params = Depends()):
    messages, total = await crud_message.read(database, params)
    response = MessageListSchema(items=messages, total=total)
    return response

@message_router.post('/', status_code=201, responses={400: {"model": BadRequest}})
async def post_message(message_input: MessageInput,
                       response: Response,
                       current_user: UserSchema = Depends(get_current_user)):
    if len(message_input.message.strip()) == 0:
        response.status_code = 400
        return response
    message_input.sender_id = current_user.id
    response.status_code = await crud_message.create(database, message_input)
    return response
