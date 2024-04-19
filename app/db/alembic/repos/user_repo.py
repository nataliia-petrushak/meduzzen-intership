
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.schemas.users import UserSignUp, UserUpdate
from app.db.models import User
from app.db.alembic.repos.base_repo import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserBase)

    async def create_model(self, db: AsyncSession, model_data: UserSignUp) -> UserBase:
        model_data = model_data.model_dump()
        query = insert(self.model).values(**model_data)
        result = await db.execute(query)
        await db.commit()
        logger.info(f"User {result.inserted_primary_key} has been created")
        return {**model_data, "id": result.inserted_primary_key}

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: UserUpdate
    ) -> User:
        model_data = model_data.model_dump(exclude_unset=True)
        model = await self.get_model_by_id(db=db, model_id=model_id)
        query = update(self.model).where(self.model.id == model_id).values(**model_data)

        await db.execute(query)
        await db.commit()
        logger.info(f"User {model.id} has been updated")
        return model

    async def delete_model(self, db: AsyncSession, model_id: int) -> None:
        model = await self.get_model_by_id(db=db, model_id=model_id)
        await db.execute(delete(self.model).filter(self.model.id == model_id))
        await db.commit()
        logger.info(f"User {model.id} has been deleted")


user_repository = UserRepository()
