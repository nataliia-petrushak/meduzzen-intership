from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AccessDeniedError, ValidationError, ObjectNotFound
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.quiz_repo import QuizRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.db.models import RequestType
from app.dependencies import check_permissions
from app.schemas.quiz import QuizCreate, GetQuiz, QuizUpdate
from app.schemas.users import GetUser


class QuizService:
    def __init__(self) -> None:
        self._quiz_repo = QuizRepository()
        self._company_repo = CompanyRepository()
        self._request_repo = RequestRepository()

    async def check_user(
        self, db: AsyncSession, company_id: UUID, user: GetUser
    ) -> None:
        try:
            request = await self._request_repo.get_model_by(
                db=db, filters={"user_id": user.id, "company_id": company_id}
            )
            if request.request_type != RequestType.admin:
                raise AccessDeniedError()
        except ObjectNotFound:
            company = await self._company_repo.get_model_by(
                db=db, filters={"id": company_id}
            )
            check_permissions(user_id=company.owner_id, user=user)

    @staticmethod
    def validate_quiz(quiz: dict) -> dict:
        if len(quiz["questions"]) < 2:
            raise ValidationError(detail="Questions should be at least 2")

        for question in quiz["questions"]:
            if len(question["answers"]) < 2:
                raise ValidationError(detail="Answers should be at least 2")

        return quiz

    async def create_quiz(
        self, company_id: UUID, quiz_data: QuizCreate, user: GetUser, db: AsyncSession
    ) -> GetQuiz:
        await self.check_user(db=db, company_id=company_id, user=user)

        model_data = self.validate_quiz(quiz_data.model_dump())
        model_data["company_id"] = company_id

        return await self._quiz_repo.create_model(db=db, model_data=model_data)

    async def update_quiz(
        self,
        company_id: UUID,
        quiz_id: UUID,
        quiz_data: QuizUpdate,
        user: GetUser,
        db: AsyncSession,
    ) -> GetQuiz:
        await self.check_user(db=db, company_id=company_id, user=user)

        model_data = quiz_data.model_dump(exclude_unset=True)
        if model_data["questions"]:
            model_data = self.validate_quiz(model_data)
        return await self._quiz_repo.update_model(
            db=db, model_data=model_data, model_id=quiz_id
        )

    async def get_quiz_list(
        self,
        company_id: UUID,
        user: GetUser,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> list[GetQuiz]:
        await self.check_user(db=db, company_id=company_id, user=user)
        return await self._quiz_repo.get_model_list(
            db=db, offset=offset, limit=limit, filters={"company_id": company_id}
        )

    async def delete_quiz(
        self, company_id: UUID, user: GetUser, db: AsyncSession, quiz_id: UUID
    ) -> None:
        await self.check_user(db=db, company_id=company_id, user=user)
        await self._quiz_repo.delete_model(db=db, model_id=quiz_id)
