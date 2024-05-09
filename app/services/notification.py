from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ObjectNotFound
from app.db.alembic.repos.notification import NotificationRepository
from app.db.alembic.repos.quiz_result_repo import QuizResultRepository
from app.db.models import NotificationStatus
from app.permissions import check_permissions
from app.schemas.notification import GetNotification, OverdueQuiz
from app.schemas.users import GetUser
from app.logger import custom_logger


class NotificationService:
    def __init__(self) -> None:
        self._notification_repo = NotificationRepository()
        self._result_repo = QuizResultRepository()

    async def change_notification_status(
            self,
            notification_id: UUID,
            user_id: UUID,
            user: GetUser,
            db: AsyncSession,
            notification_status: NotificationStatus
    ) -> GetNotification:
        check_permissions(user_id=user_id, user=user)
        return await self._notification_repo.update_model(
            db=db, model_data={"notification_status": notification_status}, model_id=notification_id
        )

    async def user_get_notification_list(
            self, user_id: UUID, user: GetUser, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[GetNotification]:
        check_permissions(user_id=user_id, user=user)
        return await self._notification_repo.get_model_list(
            db=db, filters={"user_id": user_id}, limit=limit, offset=offset
        )

    async def get_overdue_quiz_list(self, db: AsyncSession) -> list[OverdueQuiz]:
        results = await self._result_repo.get_overdue_quiz_results(db=db)
        return [
            OverdueQuiz(
                quiz_id=quiz_id, user_id=user_id, user_email=user_email
            ) for quiz_id, user_id, user_email in results
        ]

    async def check_notification_sent(self, user_id: UUID, quiz_id: UUID, db: AsyncSession) -> bool:
        try:
            await self._notification_repo.get_model_by(
                db=db, filters={"user_id": user_id, "quiz_id": quiz_id, "notification_type": "reminder"}
            )
            return True
        except ObjectNotFound:
            return False

    async def send_reminder_notifications(self, db: AsyncSession):
        users_data = await self.get_overdue_quiz_list(db=db)
        for user_data in users_data:
            is_sent = await self.check_notification_sent(
                user_id=user_data.user_id, quiz_id=user_data.quiz_id, db=db)
            if not is_sent:
                custom_logger.info(f"Sending notification to {user_data.user_id}")
                await self._notification_repo.create_model(
                    db=db, model_data={
                        "user_id": user_data.user_id,
                        "quiz_id": user_data.quiz_id,
                        "notification_type": "reminder",
                        "message": f"You have finished quiz - "
                                   f"{user_data.quiz_id} too long ago, please try again"
                    }
                )
