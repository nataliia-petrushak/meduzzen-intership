import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from app.routers import health, user
from app.config import settings
from app.core.exceptions import ObjectNotFound

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins)
app.include_router(health.router)
app.include_router(user.router)


@app.exception_handler(ObjectNotFound)
async def user_not_found_handler(request: Request, exc: ObjectNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"message": exc.msg}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
