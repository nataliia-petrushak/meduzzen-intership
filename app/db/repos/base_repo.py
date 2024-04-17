from typing import List
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.db.models import Base
from services.security import password_helper
from starlette import status


class BaseRepository:
    def __init__(self, model: Base) -> None:
        self.model = model

    async def get_model_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> List[Base]:
        query = select(self.model).offset(offset).limit(limit)
        models = await db.execute(query)
        return [model[0] for model in models.fetchall()]

    async def get_model_by_id(self, db: AsyncSession, model_id: UUID) -> Base | None:
        result = await db.execute(select(self.model).where(self.model.id == model_id))
        model = result.scalars().one_or_none()

        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
            )

        return model

    async def create_model(self, db: AsyncSession, model_data: BaseModel) -> Base:
        query = insert(self.model).values(
            username=model_data.username,
            email=model_data.email,
            password=password_helper.hash_password(model_data.password),
        )
        result = await db.execute(query)
        await db.commit()
        logger.info(f"User {result.inserted_primary_key} has been created")
        return {**model_data.model_dump(), "id": result.inserted_primary_key}

    async def update_model(
        self, db: AsyncSession, model_id: UUID, model_data: BaseModel
    ) -> Base:
        db_model = await self.get_model_by_id(db, model_id)
        model_data = model_data.model_dump(exclude_unset=True)

        if "password" in model_data:
            model_data["password"] = password_helper.hash_password(
                model_data["password"]
            )

        query = update(self.model).where(self.model.id == model_id).values(**model_data)

        await db.execute(query)
        await db.commit()
        logger.info(f"User {db_model.id} has been updated")
        return db_model

    async def delete_model(self, db: AsyncSession, model_id: UUID) -> dict:
        db_model = await self.get_model_by_id(db, model_id)

        await db.execute(delete(self.model).where(self.model.id == model_id))
        await db.commit()
        logger.info(f"User {db_model.id} has been deleted")
        return {"message": "User has been deleted successfully"}
