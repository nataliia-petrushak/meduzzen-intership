from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import StreamingResponse

from app.db.database import get_db
from app.schemas.quiz_result import GetQuizResult, Answers, Rating, RedisResult
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.quiz_result import QuizResultService

router = APIRouter(prefix="/result", tags=["result"])


@router.post(
    "/{quiz_id}",
    response_model=GetQuizResult,
    status_code=status.HTTP_200_OK
)
async def post_quiz_result(
        quiz_id: UUID,
        answers: list[Answers],
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        result_service: QuizResultService = Depends(QuizResultService)
) -> GetQuizResult:
    return await result_service.get_quiz_results(
        db=db, quiz_id=quiz_id, answers=answers, user=user
    )


@router.get("/{user_id}/total_rating", response_model=Rating, status_code=status.HTTP_200_OK)
async def get_user_total_rating(
        user_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        result_service: QuizResultService = Depends(QuizResultService)
) -> Rating:
    return await result_service.count_rating_for_user(
        db=db, user_id=user_id, user=user
    )


@router.get("/{user_id}/company/{company_id}", response_model=Rating, status_code=status.HTTP_200_OK)
async def get_user_company_rating(
        user_id: UUID,
        company_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        result_service: QuizResultService = Depends(QuizResultService)
) -> Rating:
    return await result_service.count_rating_for_user(
        db=db, user_id=user_id, company_id=company_id, user=user
    )


@router.get(
    "/{user_id}/cached_results",
    response_model=list[RedisResult] | None,
    status_code=status.HTTP_200_OK)
async def get_cached_results(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        result_service: QuizResultService = Depends(QuizResultService),
        csv: bool = False,
) -> list[RedisResult] | StreamingResponse:
    return await result_service.user_get_cashed_data(user_id=user_id, db=db, user=user, csv=csv)


@router.get(
    "/{company_id}/cached_results",
    response_model=list[RedisResult] | None,
    status_code=status.HTTP_200_OK
    )
async def company_get_cached_results(
        company_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        result_service: QuizResultService = Depends(QuizResultService),
        user_id: UUID = None,
        quiz_id: UUID = None,
        csv: bool = False
) -> list[RedisResult] | StreamingResponse:
    return await result_service.company_get_cashed_data(
        db=db, user=user, company_id=company_id, csv=csv, user_id=user_id, quiz_id=quiz_id
    )
