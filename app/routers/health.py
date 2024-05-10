from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.get("/")
async def health_check() -> dict:
    return {"status_code": status.HTTP_200_OK, "detail": "ok", "result": "working"}
