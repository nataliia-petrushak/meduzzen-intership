import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, user
from app.config import settings
from app.utils.common import UserNotFound

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins)

app.include_router(health.router)
app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
