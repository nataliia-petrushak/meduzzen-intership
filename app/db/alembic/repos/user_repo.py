from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.schemas.users import UserSignUp, UserUpdate
from app.db.models import User
from app.db.alembic.repos.base_repo import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def create_model(self, db: AsyncSession, model_data: UserSignUp) -> User:
        model_data = model_data.model_dump(exclude_unset=True)
        result = await BaseRepository.create_model(self, db=db, model_data=model_data)
        logger.info(f"User {result.id} has been created")
        return result

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: UserUpdate
    ) -> User:
        model_data = model_data.model_dump(exclude_unset=True)
        result = await BaseRepository.update_model(
            self, db=db, model_id=model_id, model_data=model_data
        )
        logger.info(f"User {model_id} has been updated")
        return result

    async def delete_model(self, db: AsyncSession, model_id: UUID) -> None:
        await BaseRepository.delete_model(self, db=db, model_id=model_id)
        logger.info(f"User {model_id} has been deleted")


user_repository = UserRepository()
