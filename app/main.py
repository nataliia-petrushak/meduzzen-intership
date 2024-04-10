import uvicorn
from fastapi import FastAPI

from routers import health
from config import settings

app = FastAPI()
app.include_router(health.router)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
