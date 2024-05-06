from typing import TextIO
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
import pandas as pd

from app.core.exceptions import AccessDeniedError, ObjectNotFound
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.quiz_repo import QuizRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.db.alembic.repos.quiz_result_repo import QuizResultRepository
from app.db.models import RequestType
from app.db.redis import DBRedisManager
from app.permissions import check_permissions
from app.schemas.quiz import GetQuiz
from app.schemas.quiz_result import Answers, GetQuizResult, Rating, RedisResult
from app.schemas.users import GetUser


class QuizResultService:
    def __init__(self) -> None:
        self._quiz_result_repo = QuizResultRepository()
        self._request_repo = RequestRepository()
        self._quiz_repo = QuizRepository()
        self._company_repo = CompanyRepository()
        self._redis = DBRedisManager()

    async def check_user_is_member(self, user: GetUser, company_id: UUID, db: AsyncSession) -> None:
        try:
            self._request_repo.get_model_by(db=db, filters={
                    "user_id": user.id,
                    "company_id": company_id,
                    "request_type": RequestType.member
                }
            )
        except ObjectNotFound:
            raise AccessDeniedError()

    async def check_user_is_admin_or_owner(
            self, db: AsyncSession, company_id: UUID, user: GetUser
    ) -> None:
        try:
            request = await self._request_repo.get_model_by(
                db=db, filters={"company_id": company_id, "user_id": user.id, "request_type": "admin"}
            )
        except ObjectNotFound:
            request = None

        company = await self._company_repo.get_model_by(db=db, filters={"id": company_id})
        if not request and company.owner_id != user.id:
            raise AccessDeniedError()

    async def check_user_did_quiz_before(
            self, quiz_id: UUID, db: AsyncSession, user: GetUser
    ) -> GetQuizResult | None:
        try:
            quiz_result = await self._quiz_result_repo.get_model_by(
                db=db, filters={"user_id": user.id, "quiz_id": quiz_id}
            )
            return quiz_result
        except ObjectNotFound:
            return None

    async def update_quiz_result(
            self, result: GetQuizResult, quiz: GetQuiz, num_corr_answers: int, db: AsyncSession
    ) -> GetQuizResult:
        all_results = result.all_results
        all_results.append({
            "num_corr_answers": num_corr_answers,
            "questions_count": len(quiz.questions)
        })
        return await self._quiz_result_repo.update_model(db=db, model_id=result.id, model_data={
            "all_results": all_results
        })

    async def create_or_update_result(
            self, quiz: GetQuiz, user: GetUser, db: AsyncSession, num_corr_answers: int
    ) -> GetQuizResult:
        previous_result = await self.check_user_did_quiz_before(quiz_id=quiz.id, user=user, db=db)
        if previous_result:
            return await self.update_quiz_result(
                db=db, result=previous_result, num_corr_answers=num_corr_answers, quiz=quiz
            )

        return await self._quiz_result_repo.create_model(
            db=db,
            model_data={
                "user_id": user.id,
                "company_id": quiz.company_id,
                "quiz_id": quiz.id,
                "all_results": [{
                    "num_corr_answers": num_corr_answers,
                    "questions_count": len(quiz.questions)
                }]
            }
        )

    async def get_quiz_results(
            self,
            db: AsyncSession,
            quiz_id: UUID,
            user: GetUser,
            answers: list[Answers]
    ) -> GetQuizResult:
        quiz = await self._quiz_repo.get_model_by(db=db, filters={"id": quiz_id})
        num_corr_answers = len([answer for answer in answers if answer.is_correct])
        await self.check_user_is_member(db=db, user=user, company_id=quiz.company_id)

        await self._quiz_repo.update_model(
            db=db, model_id=quiz.id, model_data={"num_done": quiz.num_done + 1}
        )

        redis_data = {"user": user, "company": quiz.company, "quiz": quiz, "answers": answers}
        result = await self.create_or_update_result(
            quiz=quiz, user=user, db=db, num_corr_answers=num_corr_answers
        )
        await self._redis.set_value(f"result_{result.id}", redis_data)
        return result

    async def count_rating_for_user(
            self, db: AsyncSession, user_id: UUID, user: GetUser, company_id: UUID = None
    ) -> Rating:
        check_permissions(user_id=user_id, user=user)

        filters = {"user_id": user_id}
        if company_id:
            filters["company_id"] = company_id

        data = await self._quiz_result_repo.get_user_results_records(
            db=db, filters=filters
        )

        all_num_corr_answers = sum(result["num_corr_answers"] for result in data)
        all_questions_count = sum(result["questions_count"] for result in data)
        if not all_questions_count:
            return Rating(rating=None)

        rating = round(all_num_corr_answers / all_questions_count, 3)
        return Rating(rating=rating)

    async def get_data_from_redis(self, result_list: list[GetQuizResult]) -> list[dict]:
        data = []
        for result in result_list:
            redis_res = await self._redis.get_value(f"result_{result.id}")
            redis_res = redis_res.get("value")
            if redis_res:
                redis_res["user"] = redis_res["user"].__dict__
                redis_res["company"] = redis_res["company"].__dict__
                redis_res["quiz"] = redis_res["quiz"].__dict__
                data.append(redis_res)
        return data

    @staticmethod
    async def data_to_csv(data: list[dict]) -> StreamingResponse:
        df = pd.DataFrame(data, columns=["user", "company", "quiz", "answers"])
        return StreamingResponse(
            iter(df.to_csv(index=False)),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=data.csv"}
        )

    async def user_get_cashed_data(
            self,
            db: AsyncSession,
            user: GetUser,
            user_id: UUID,
            csv: bool = False,
    ) -> list[dict] | StreamingResponse:
        check_permissions(user_id=user_id, user=user)
        user_results = await self._quiz_result_repo.get_model_list(db=db, filters={"user_id": user_id})
        data = await self.get_data_from_redis(result_list=user_results)
        if csv:
            return await self.data_to_csv(data)
        return data

    async def company_get_cashed_data(
            self,
            db: AsyncSession,
            user: GetUser,
            company_id: UUID,
            csv: bool = False,
            **kwargs
    ) -> list[dict] | StreamingResponse:
        await self.check_user_is_admin_or_owner(company_id=company_id, user=user, db=db)
        filters = {kwargs[key]: kwargs[value] for key, value in kwargs.items() if kwargs[value] is not None}
        filters["company_id"] = company_id
        results = await self._quiz_result_repo.get_model_list(db=db, filters=filters)
        data = await self.get_data_from_redis(result_list=results)
        if csv:
            return await self.data_to_csv(data)
        return data
