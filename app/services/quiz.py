import json
from uuid import UUID

import pandas as pd
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AccessDeniedError, ObjectNotFound, NoResultsError, ObjectAlreadyExistError
from app.db.alembic.repos.company_repo import CompanyRepository
from app.db.alembic.repos.notification import NotificationRepository
from app.db.alembic.repos.quiz_repo import QuizRepository
from app.db.alembic.repos.request_repo import RequestRepository
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

    async def create_quiz_notifications(
        self, db: AsyncSession, quiz_id: UUID, company_id: UUID
    ) -> None:
        members = await self._request_repo.get_model_list(
            db=db, filters={"request_type": "member", "company_id": company_id}
        )
        for member in members:
            await self._notification_repo.create_model(
                db=db,
                model_data={
                    "user_id": member.user_id,
                    "quiz_id": quiz_id,
                    "message": f"Your company created a new "
                               f"quiz - {quiz_id}. Try to finish it",
                },
            )

    async def check_quiz_exist_in_company(self, name: str, company_id: UUID, db: AsyncSession) -> None:
        try:
            await self._quiz_repo.get_model_by(db=db, filters={"name": name, "company_id": company_id})
            raise ObjectAlreadyExistError(model_name="Quiz", identifier=name)
        except ObjectNotFound:
            return None

    async def create_quiz(
        self, company_id: UUID, quiz_data: QuizCreate, user: GetUser, db: AsyncSession
    ) -> GetQuiz:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        await self.check_quiz_exist_in_company(db=db, company_id=company_id, name=quiz_data.name)
        model_data = quiz_data.model_dump()
        model_data["company_id"] = company_id

        quiz = await self._quiz_repo.create_model(db=db, model_data=model_data)
        await self.create_quiz_notifications(
            db=db, company_id=company_id, quiz_id=quiz.id
        )
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
        db: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> list[GetQuiz]:
        quizzes = await self._quiz_repo.get_model_list(
            db=db, offset=offset, limit=limit, filters={"company_id": company_id}
        )
        if not quizzes:
            raise NoResultsError()
        return quizzes

    async def delete_quiz(
        self, company_id: UUID, user: GetUser, db: AsyncSession, quiz_id: UUID
    ) -> None:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        await self._quiz_repo.delete_model(db=db, model_id=quiz_id)

    async def upload_quiz_from_excel(
            self,
            file: UploadFile,
            db: AsyncSession,
            company_id: UUID,
            user: GetUser
    ) -> list[GetQuiz]:
        await self.check_user_is_admin_or_owner(db=db, company_id=company_id, user=user)
        content = await file.read()
        quiz_data = pd.read_excel(content)
        result = []
        for _, data in quiz_data.iterrows():
            data["questions"] = json.loads(data["questions"])
            if "quiz_id" in data:
                quiz_id = UUID(data.pop("quiz_id"))
                quiz = await self._quiz_repo.update_model(
                    db=db, model_data=data, model_id=quiz_id
                )
            else:
                data["company_id"] = company_id
                quiz = await self._quiz_repo.create_model(db=db, model_data=data)
            result.append(quiz)
        return result
