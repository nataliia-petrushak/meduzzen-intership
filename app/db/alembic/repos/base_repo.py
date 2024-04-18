from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base
from starlette import status


class BaseRepository:
    def __init__(self, model: Base) -> None:
        self.model = model

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> list[Base]:
        query = select(self.model).offset(offset).limit(limit)
        models = await db.execute(query)
        return [model[0] for model in models.fetchall()]

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> Base | None:
        result = await db.execute(select(self.model).filter(self.model.id == model_id))
        model = result.scalar()

        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
            )

        return model

    async def create_model(self, db: AsyncSession, model_data: dict) -> Base:
        query = insert(self.model).values(**model_data)
        result = await db.execute(query)
        await db.commit()
        return {**model_data, "id": result.inserted_primary_key}

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: dict
    ) -> Base:
        model = await self.get_model_by_id(db=db, model_id=model_id)
        query = (
            update(self.model).filter(self.model.id == model_id).values(**model_data)
        )

        await db.execute(query)
        await db.commit()
        return model

    async def delete_model(self, db: AsyncSession, model_id: UUID) -> None:
        await self.get_model_by_id(db=db, model_id=model_id)
        await db.execute(delete(self.model).filter(self.model.id == model_id))
        await db.commit()
