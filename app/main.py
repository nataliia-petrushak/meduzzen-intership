import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import health
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=settings.allowed_origins
)

app.include_router(health.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
