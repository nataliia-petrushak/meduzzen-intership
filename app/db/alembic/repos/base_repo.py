from uuid import UUID

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base
from app.utils.common import UserNotFound


class BaseRepository:
    def __init__(self, model: Base) -> None:
        self.model = model

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[Base]:
        query = select(self.model).offset(offset).limit(limit)
        models = await db.execute(query)
        return [model[0] for model in models.fetchall()]

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> Base:
        result = await db.execute(
            select(self.model, self.model.id).filter(self.model.id == model_id)
        )
        model = result.scalar()

        if not model:
            raise UserNotFound(object_id=model_id)

        return model

    async def create_model(self, db: AsyncSession, model_data: dict) -> Base:
        query = insert(self.model).values(**model_data).returning(self.model)
        result = await db.execute(query)
        await db.commit()
        return result.scalars().one_or_none()

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: dict
    ) -> Base:
        result = await db.execute(
            update(self.model)
            .where(self.model.id == model_id)
            .values(**model_data)
            .returning(self.model)
        )
        await db.commit()
        model = result.scalar()

        if not model:
            raise UserNotFound(object_id=model_id)
        return model

    async def delete_model(self, db: AsyncSession, model_id: UUID) -> Base:
        result = await db.execute(
            delete(self.model).where(self.model.id == model_id).returning(self.model)
        )
        await db.commit()
        model = result.scalar()
        if not model:
            raise UserNotFound(object_id=model_id)
        return model
