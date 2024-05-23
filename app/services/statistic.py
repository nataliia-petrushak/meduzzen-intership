from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound, AccessDeniedError, NoResultsError
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.quiz_repo import QuizRepository
from app.db.alembic.repos.quiz_result_repo import QuizResultRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.schemas.statistic import (
    AvgScoreWithTime,
    QuizWithCompleteTime,
    UsersQuizCompleteTime,
)
from app.schemas.users import GetUser


class StatisticService:
    def __init__(self) -> None:
        self._quiz_repo = QuizRepository()
        self._result_repo = QuizResultRepository()
        self._request_repo = RequestRepository()
        self._company_repo = CompanyRepository()

    async def check_user_is_admin_or_owner(
        self, db: AsyncSession, company_id: UUID, user: GetUser
    ) -> None:
        try:
            request = await self._request_repo.get_model_by(
                db=db,
                filters={
                    "company_id": company_id,
                    "user_id": user.id,
                    "request_type": "admin",
                },
            )
        except ObjectNotFound:
            request = None

        company = await self._company_repo.get_model_by(
            db=db, filters={"id": company_id}
        )
        if not request and company.owner_id != user.id:
            raise AccessDeniedError()

    async def average_score_dynamic(
        self, db: AsyncSession, **kwargs
    ) -> list[AvgScoreWithTime]:
        filters = {key: value for key, value in kwargs.items() if value}
        data = await self._result_repo.get_results_records(db=db, filters=filters)
        result = []
        corr_answers, all_questions = 0, 0
        for data in data:
            corr_answers += data["num_corr_answers"]
            all_questions += data["questions_count"]
            avg_score = AvgScoreWithTime(
                date=data["date"], score=round(corr_answers / all_questions, 3)
            )
            result.append(avg_score)
        if not result:
            raise NoResultsError()
        return result

    async def user_avg_score_dynamic(
        self, db: AsyncSession, user: GetUser
    ) -> list[AvgScoreWithTime]:
        results = await self.average_score_dynamic(db=db, user_id=user.id)
        if not results:
            raise NoResultsError()
        return results

    async def company_avg_score_dynamic(
        self, db: AsyncSession, user: GetUser, company_id: UUID, user_id: UUID = None
    ) -> list[AvgScoreWithTime]:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        results = await self.average_score_dynamic(
            db=db, user_id=user_id, company_id=company_id
        )
        if not results:
            raise NoResultsError()
        return results

    async def quiz_list_with_last_completion_time(
        self, db: AsyncSession, user: GetUser
    ) -> list[QuizWithCompleteTime]:
        user_results = await self._result_repo.get_model_list(
            db=db, filters={"user_id": user.id}
        )
        if not user_results:
            raise NoResultsError()
        return [
            QuizWithCompleteTime(
                quiz_id=result.quiz_id, date=result.all_results[-1]["date"]
            ) for result in user_results
        ]

    async def company_users_with_last_quiz_completion_time(
        self, db: AsyncSession, company_id: UUID, quiz_id: UUID, user: GetUser
    ) -> list[UsersQuizCompleteTime]:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        quiz_results = await self._result_repo.get_model_list(
            db=db, filters={"company_id": company_id, "quiz_id": quiz_id}
        )
        if not quiz_results:
            raise NoResultsError()
        return [
            UsersQuizCompleteTime(
                user_id=result.user_id, date=result.all_results[-1]["date"]
            ) for result in quiz_results
        ]
