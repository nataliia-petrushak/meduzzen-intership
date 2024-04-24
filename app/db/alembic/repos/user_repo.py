from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFound
from app.db.models import User
from app.db.alembic.repos.base_repo import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        result = await db.execute(select(self.model).filter(self.model.email == email))
        user = result.scalar()

        if not user:
            raise UserNotFound(identifier=email)
        return user

    async def user_deactivate(self, db: AsyncSession, user_id: UUID) -> User:
        result = await db.execute(
            update(self.model)
            .where(self.model.id == user_id)
            .values(is_active=False)
            .returning(self.model)
        )
        await db.commit()
        return result.scalar()
