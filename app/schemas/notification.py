from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.db.models import NotificationStatus


class NotificationBase(BaseModel):
    message: str


class NotificationCreate(NotificationBase):
    user_id: UUID
    quiz_id: UUID


class GetNotification(NotificationBase):
    id: UUID
    user_id: UUID
    quiz_id: UUID
    notification_status: NotificationStatus


class OverdueQuiz(BaseModel):
    quiz_id: UUID
    user_id: UUID
    user_email: EmailStr