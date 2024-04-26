import uuid

from sqlalchemy import String, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class IDBase(Base):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class User(IDBase):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
