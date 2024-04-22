from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFound
from app.db.models import User
from app.db.alembic.repos.base_repo import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(self.model).filter(self.model.email == email))
        user = result.scalar()

        if not user:
            raise UserNotFound(object_id=email)
        return user
