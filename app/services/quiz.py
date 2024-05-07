from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AccessDeniedError, ObjectNotFound
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.notification import NotificationRepository
from app.db.alembic.repos.quiz_repo import QuizRepository
from app.db.alembic.repos.request_repo import RequestRepository
from app.db.models import RequestType
from app.permissions import check_permissions
from app.schemas.quiz import QuizCreate, GetQuiz, QuizUpdate
from app.schemas.users import GetUser


class QuizService:
    def __init__(self) -> None:
        self._quiz_repo = QuizRepository()
        self._company_repo = CompanyRepository()
        self._request_repo = RequestRepository()
        self._notification_repo = NotificationRepository()

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

    async def create_quiz_notifications(self, db: AsyncSession, quiz_id: UUID, company_id: UUID) -> None:
        members = await self._request_repo.request_list(
            db=db, request_type="member", company_id=company_id
        )
        for member in members:
            await self._notification_repo.create_model(
                db=db,
                model_data={
                    "user_id": member.id,
                    "message": f"Your company created a new quiz - {quiz_id}. Try to finish it"
                }
            )

    async def create_quiz(
        self, company_id: UUID, quiz_data: QuizCreate, user: GetUser, db: AsyncSession
    ) -> GetQuiz:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        model_data = quiz_data.model_dump()
        model_data["company_id"] = company_id

        quiz = await self._quiz_repo.create_model(db=db, model_data=model_data)
        await self.create_quiz_notifications(db=db, company_id=company_id, quiz_id=quiz.id)
        return quiz

    async def update_quiz(
        self,
        company_id: UUID,
        quiz_id: UUID,
        quiz_data: QuizUpdate,
        user: GetUser,
        db: AsyncSession,
    ) -> GetQuiz:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)

        model_data = quiz_data.model_dump(exclude_unset=True)
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
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        return await self._quiz_repo.get_model_list(
            db=db, offset=offset, limit=limit, filters={"company_id": company_id}
        )

    async def delete_quiz(
        self, company_id: UUID, user: GetUser, db: AsyncSession, quiz_id: UUID
    ) -> None:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        await self._quiz_repo.delete_model(db=db, model_id=quiz_id)
