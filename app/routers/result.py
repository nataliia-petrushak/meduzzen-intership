from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.schemas.result import GetResult, Answers, Rating
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.result import ResultService

router = APIRouter(prefix="/result", tags=["result"])


@router.post(
    "/{quiz_id}",
    response_model=GetResult,
    status_code=status.HTTP_200_OK
)
async def send_answers_and_get_quiz_result(
        quiz_id: UUID,
        answers: list[Answers],
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        result_service: ResultService = Depends(ResultService)
) -> GetResult:
    return await result_service.get_quiz_results(
        db=db, quiz_id=quiz_id, answers=answers, user=user
    )


@router.get("/{user_id}/total_rating", response_model=Rating, status_code=status.HTTP_200_OK)
async def get_user_total_rating(
        user_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        db: AsyncSession = Depends(get_db),
        result_service: ResultService = Depends(ResultService)
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
        result_service: ResultService = Depends(ResultService)
) -> Rating:
    return await result_service.count_rating_for_user(
        db=db, user_id=user_id, company_id=company_id, user=user
    )
