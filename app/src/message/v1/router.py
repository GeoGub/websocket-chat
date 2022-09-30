from fastapi import APIRouter, Depends, Response

from src.database import database
from src.sample_schemas import Params, BadRequest


message_router = APIRouter(prefix='/messages')

@message_router.get('/')
def get_messages():
    return

@message_router.post('/')
def post_message(sel: int):
    return
