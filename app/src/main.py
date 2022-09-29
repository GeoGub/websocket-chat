from fastapi import FastAPI

from src.database import database
from src.auth.v1.router import auth_router
from src.user.v1.router import user_router
from src.chat.v1.router import chat_router
from src.message.v1.router import message_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
