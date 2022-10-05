from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import database
from src.auth.v1.router import auth_router
from src.user.v1.router import user_router
from src.message.v1.router import message_router
from src.websocket.v1.router import websocket_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(message_router)
app.include_router(websocket_router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
