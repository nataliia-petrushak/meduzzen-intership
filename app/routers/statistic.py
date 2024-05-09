from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.schemas.statistic import AvgScoreWithTime, QuizWithCompleteTime, UsersQuizCompleteTime
from app.schemas.users import GetUser
from app.services.auth import get_authenticated_user
from app.services.statistic import StatisticService

router = APIRouter(tags=["statistic"], prefix="/statistic")


@router.get(
    "/{user_id}/avg_score_dynamics",
    response_model=list[AvgScoreWithTime],
    status_code=status.HTTP_200_OK
)
async def get_user_avg_dynamic(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        statistic_service: StatisticService = Depends(StatisticService)
) -> list[AvgScoreWithTime]:
    return await statistic_service.user_avg_score_dynamic(
        db=db, user_id=user_id, user=user
    )


@router.get(
    "/{company_id}/avg_score_dynamic",
    response_model=list[AvgScoreWithTime],
    status_code=status.HTTP_200_OK
)
async def get_company_all_users_avg_dynamic(
        company_id: UUID,
        user_id: UUID = None,
        db: AsyncSession = Depends(get_db),
        user: GetUser = Depends(get_authenticated_user),
        statistic_service: StatisticService = Depends(StatisticService),
) -> list[AvgScoreWithTime]:
    return await statistic_service.company_avg_score_dynamic(
        db=db, company_id=company_id, user_id=user_id, user=user
    )


@router.get(
    "/{user_id}/quizzes",
    response_model=list[QuizWithCompleteTime],
    status_code=status.HTTP_200_OK
)
async def get_quiz_last_comp_time(
        user_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        statistic_service: StatisticService = Depends(StatisticService),
        db: AsyncSession = Depends(get_db)
) -> list[QuizWithCompleteTime]:
    return await statistic_service.quiz_list_with_last_completion_time(
        db=db, user_id=user_id, user=user
    )


@router.get(
    "/{company_id}/quiz/{quiz_id}/users",
    response_model=list[UsersQuizCompleteTime],
    status_code=status.HTTP_200_OK
)
async def get_users_last_comp_time_for_quiz(
        company_id: UUID,
        quiz_id: UUID,
        user: GetUser = Depends(get_authenticated_user),
        statistic_service: StatisticService = Depends(StatisticService),
        db: AsyncSession = Depends(get_db)
) -> list[UsersQuizCompleteTime]:
    return await statistic_service.company_users_with_last_quiz_completion_time(
        db=db, company_id=company_id, quiz_id=quiz_id, user=user
    )
