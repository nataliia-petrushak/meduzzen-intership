from fastapi import FastAPI
from starlette import status
from functools import lru_cache

from app import config

app = FastAPI()


@lru_cache
def get_settings():
    return config.Settings()


@app.get("/")
async def health_check() -> dict:
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "ok",
        "result": "working"
    }
