import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import String, UUID, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from sqlalchemy.ext.mutable import MutableList

from app.db.database import Base


class RequestType(Enum):
    join_request = "join_request"
    invitation = "invitation"
    member = "member"
    admin = "admin"


class NotificationStatus(Enum):
    unread = "unread"
    read = "read"


class IDBase(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class User(IDBase):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)


class Company(IDBase):
    __tablename__ = "company"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String(500))
    is_hidden: Mapped[bool] = mapped_column(Boolean(), default=False)

    owner: Mapped[User] = Relationship("User", lazy="selectin")


class Request(IDBase):
    __tablename__ = "request"

    request_type: Mapped[RequestType] = mapped_column(
        ENUM(RequestType, name="request_type"), nullable=False
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    company: Mapped[Company] = Relationship("Company", lazy="selectin")
    user: Mapped[User] = Relationship("User", lazy="selectin")


class Quiz(IDBase):
    __tablename__ = "quiz"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    num_done: Mapped[int] = mapped_column(Integer(), default=0)
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    questions: Mapped[JSONB] = mapped_column(
        MutableList.as_mutable(JSONB()), nullable=False
    )

    company: Mapped[Company] = Relationship("Company", lazy="selectin")


class QuizResult(IDBase):
    __tablename__ = "quiz_result"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    quiz_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    all_results: Mapped[JSONB] = mapped_column(MutableList.as_mutable(JSONB()), nullable=False)

    user: Mapped[User] = Relationship("User", lazy="selectin")
    quiz: Mapped[Quiz] = Relationship("Quiz", lazy="selectin")
    company: Mapped[Company] = Relationship("Company", lazy="selectin")


class Notification(IDBase):
    __tablename__ = "notification"

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    quiz_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False
    )
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    notification_status: Mapped[NotificationStatus] = mapped_column(
        ENUM(NotificationStatus, name="notification_status"), default="unread"
    )

    user: Mapped[User] = Relationship("User", lazy="selectin")
    quiz: Mapped[Quiz] = Relationship("Quiz", lazy="selectin")
