from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1
    database_url: str = "postgresql://postgres:root@127.0.0.1/websocket"
    redis_host: str = "redis://localhost"
    redis_password: str = "redis"
    redis_port: int = 6379
    redis_db: int = 1
    blocklist_db: int = 0

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    settings = Settings()
    return settings