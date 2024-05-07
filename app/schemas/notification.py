from uuid import UUID

from pydantic import BaseModel

from app.db.models import NotificationStatus


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: UUID


class NotificationUpdate(BaseModel):
    status: NotificationStatus


class GetNotification(NotificationBase):
    id: UUID
    user_id: UUID
    status: NotificationStatus
