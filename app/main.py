from fastapi import FastAPI
from starlette import status


app = FastAPI()


@app.get("/")
async def health_check() -> dict:
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "ok",
        "result": "working"
    }
