import uuid
from enum import auto, Enum

from sqlalchemy import String, UUID, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from app.db.database import Base


class RequestType(Enum):
    join_request = "join_request"
    invitation = "invitation"
    member = "member"


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
