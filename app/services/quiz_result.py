from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AccessDeniedError, ObjectNotFound
from app.db.alembic.repos.quiz_repo import QuizRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.db.alembic.repos.quiz_result_repo import QuizResultRepository
from app.permissions import check_permissions
from app.schemas.quiz import GetQuiz
from app.schemas.quiz_result import Answers, GetQuizResult, Rating
from app.schemas.users import GetUser


class QuizResultService:
    def __init__(self) -> None:
        self._quiz_result_repo = QuizResultRepository()
        self._request_repo = RequestRepository()
        self._quiz_repo = QuizRepository()

    async def check_user_is_member(self, user: GetUser, company_id: UUID, db: AsyncSession) -> None:
        company_members = await self._request_repo.request_list(
            db=db, company_id=company_id, request_type="member"
        )
        if user not in company_members:
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
        await self.check_user_is_member(db=db, user=user, company_id=quiz.company_id)

        await self._quiz_repo.update_model(
            db=db, model_id=quiz.id, model_data={"num_done": quiz.num_done + 1}
        )

        num_corr_answers = self.num_correct_answers(quiz=quiz, answers=answers)
        return await self.create_or_update_result(
            quiz=quiz, user=user, db=db, num_corr_answers=num_corr_answers
        )

    async def count_rating_for_user(
            self, db: AsyncSession, user_id: UUID, user: GetUser, company_id: UUID = None
    ) -> Rating:
        check_permissions(user_id=user_id, user=user)

        filters = {"user_id": user_id}
        if company_id:
            filters["company_id"] = company_id

        all_num_corr_answers = await self._quiz_result_repo.get_user_results_records(
            db=db, param="num_corr_answers", filters=filters
        )
        all_questions_count = await self._quiz_result_repo.get_user_results_records(
            db=db, param="questions_count", filters=filters
        )

        rating = round(sum(all_num_corr_answers) / sum(all_questions_count), 3)
        return Rating(rating=rating)
