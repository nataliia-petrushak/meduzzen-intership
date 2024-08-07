from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import custom_logger
from app.db.models import Base
from app.core.exceptions import ObjectNotFound


class BaseRepository:
    def __init__(self, model: Base) -> None:
        self.model = model

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10, filters: dict = None
    ) -> list[Base]:
        query = select(self.model).offset(offset).limit(limit)
        if filters:
            query = query.filter_by(**filters)
        models = await db.execute(query)
        return [model[0] for model in models.fetchall()]

    async def get_model_by(self, db: AsyncSession, filters: dict) -> Base:
        result = await db.execute(
            select(self.model, self.model.id).filter_by(**filters)
        )
        model = result.scalar()
        identifier = list(filters.values())[0]
        if not model:
            raise ObjectNotFound(identifier=identifier, model_name=self.model.__name__)

        return model

    async def create_model(self, db: AsyncSession, model_data: BaseModel) -> Base:
        result = await db.execute(
            insert(self.model).values(**model_data).returning(self.model)
        )
        await db.commit()
        model = result.scalar()
        custom_logger.info(f"{self.model.__name__} {model.id} has been created")
        return model

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: BaseModel
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
            raise ObjectNotFound(identifier=model_id, model_name=self.model.__name__)

        custom_logger.info(f"{self.model.__name__} {model.id} has been updated")
        return model

    async def delete_model(self, db: AsyncSession, model_id: UUID) -> Base:
        result = await db.execute(
            delete(self.model).where(self.model.id == model_id).returning(self.model)
        )
        await db.commit()
        model = result.scalar()

        if not model:
            raise ObjectNotFound(identifier=model_id, model_name=self.model.__name__)

        custom_logger.info(f"{self.model.__name__} {model.id} has been deleted")
        return model
