from fastapi import FastAPI
from functools import lru_cache

from app.routers import health
from app import config

app = FastAPI()
app.include_router(health.router)


@lru_cache
def get_settings():
    return config.Settings()
