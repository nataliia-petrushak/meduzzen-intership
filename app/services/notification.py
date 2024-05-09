from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alembic.repos.notification import NotificationRepository
from app.db.models import NotificationStatus
from app.permissions import check_permissions
from app.schemas.notification import GetNotification
from app.schemas.users import GetUser


class NotificationService:
    def __init__(self) -> None:
        self._notification_repo = NotificationRepository()

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
