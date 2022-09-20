from fastapi import APIRouter

from src.database import database

user_router = APIRouter(prefix='/users')

@user_router.get('/')
async def main():
    # a = await database.fetch_all(user.select())
    return {'msg': 'hello'}