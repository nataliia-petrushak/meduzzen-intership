from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFound
from app.db.models import User
from app.schemas.users import UserSignUp, UserUpdate
from app.services.security import SecurityService
from app.db.alembic.repos.user_repo import UserRepository


class UserService:
    def __init__(self):
        self._user_repo = UserRepository()

    async def create_model(self, db: AsyncSession, model_data: UserSignUp) -> User:
        try:
            user = await self._user_repo.get_user_by_email(
                db=db, email=model_data.email
            )
            user.is_active = True
            await db.commit()
        except UserNotFound:
            model_data.password = SecurityService.hash_password(model_data.password)
            user = await self._user_repo.create_model(db=db, model_data=model_data)
        return user

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: UserUpdate
    ) -> User:
        if model_data.password:
            model_data.password = SecurityService.hash_password(model_data.password)

        result = await self._user_repo.update_model(
            db=db, model_id=model_id, model_data=model_data
        )
        return result

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[User]:
        return await self._user_repo.get_model_list(
            db, offset, limit, filters={"is_active": True}
        )

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> User:
        return await self._user_repo.get_model_by_id(db, model_id=model_id)

    async def user_deactivate(self, db: AsyncSession, user_id: UUID) -> None:
        await self._user_repo.user_deactivate(db=db, user_id=user_id)

    async def get_user_by_email(self, db: AsyncSession, email: str) -> User:
        return await self._user_repo.get_user_by_email(db=db, email=email)
