from fastapi import FastAPI

from src.database import database
from src.user.v1.router import user_router

app = FastAPI()
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
