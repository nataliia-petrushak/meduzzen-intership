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

    async def get_user_list(
        self, db: AsyncSession, offset: int = 0, limit: int = 10
    ) -> List[Base]:
        query = select(self.model).offset(offset).limit(limit)
        users = await db.execute(query)
        return [user[0] for user in users.fetchall()]

    async def get_user_by_id(self, db: AsyncSession, user_id: UUID) -> Base | None:
        result = await db.execute(select(self.model).where(self.model.id == user_id))
        user = result.scalars().one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
            )

        return user

    async def create_user(self, db: AsyncSession, user_data: BaseModel) -> Base:
        query = insert(self.model).values(
            username=user_data.username,
            email=user_data.email,
            password=password_helper.hash_password(user_data.password),
        )
        result = await db.execute(query)
        await db.commit()
        logger.info(f"User {result.inserted_primary_key} has been created")
        return {**user_data.model_dump(), "id": result.inserted_primary_key}

    async def update_user(
        self, db: AsyncSession, user_id: UUID, user_data: BaseModel
    ) -> Base:
        db_user = await self.get_user_by_id(db, user_id)
        user_data = user_data.model_dump(exclude_unset=True)

        if "password" in user_data:
            user_data["password"] = password_helper.hash_password(user_data["password"])

        query = update(self.model).where(self.model.id == user_id).values(**user_data)

        await db.execute(query)
        await db.commit()
        logger.info(f"User {db_user.id} has been updated")
        return db_user

    async def delete_user(self, db: AsyncSession, user_id: UUID) -> dict:
        db_user = await self.get_user_by_id(db, user_id)

        await db.execute(delete(self.model).where(self.model.id == user_id))
        await db.commit()
        logger.info(f"User {db_user.id} has been deleted")
        return {"message": "User has been deleted successfully"}
