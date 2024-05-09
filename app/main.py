from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from app.services.scheduler import SchedulerService
from app.config import settings
from app.routers import (
    health,
    user,
    auth,
    company,
    user_request,
    company_request,
    quiz,
    quiz_result,
    statistic,
    notification
)
from app.core.exceptions import (
    ObjectNotFound,
    AuthorizationError,
    AccessDeniedError,
    NameExistError,
    OwnerRequestError,
    AssignError,
    ValidationError,
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    service = SchedulerService()
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
    scheduler.add_job(
        service.send_reminder_notifications,
        "cron", day_of_week="mon-sun", hour=17, minute=51, second=0
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins)
app.include_router(health.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(company.router)
app.include_router(company_request.router)
app.include_router(user_request.router)
app.include_router(quiz.router)
app.include_router(quiz_result.router)
app.include_router(notification.router)
app.include_router(statistic.router)


@app.exception_handler(ObjectNotFound)
async def object_not_found_handler(request: Request, exc: ObjectNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"message": exc.msg}
    )


@app.exception_handler(NameExistError)
async def name_exist_error_handler(request: Request, exc: NameExistError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"message": exc.msg}
    )


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"message": exc.msg}
    )


@app.exception_handler(AccessDeniedError)
async def access_denied_error_handler(request: Request, exc: AccessDeniedError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"message": exc.msg}
    )


@app.exception_handler(OwnerRequestError)
async def owner_inviting_error_handler(request: Request, exc: OwnerRequestError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"message": exc.msg}
    )


@app.exception_handler(AssignError)
async def assign_inviting_error_handler(request: Request, exc: AssignError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"message": exc.msg}
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": exc.msg}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
