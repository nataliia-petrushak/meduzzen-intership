from fastapi import FastAPI

from app.routers import health
from app.config import settings

app = FastAPI()
app.include_router(health.router)
