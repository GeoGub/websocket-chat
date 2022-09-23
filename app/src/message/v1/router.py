from fastapi import APIRouter


message_router = APIRouter(prefix='/messages')

@message_router.get('/')
def read_messages():
    return

@message_router.post('/')
def create_message():
    return
