from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class AbstractUser:
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)


class User(Base, AbstractUser):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
