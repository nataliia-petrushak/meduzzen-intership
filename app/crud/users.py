from typing import List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from db.models import UserBase
from schemas import users
from services.security import password_helper
from starlette import status


async def get_user_list(
    db: AsyncSession, offset: int = 0, limit: int = 10
) -> List[UserBase]:
    query = select(UserBase).offset(offset).limit(limit)
    users = await db.execute(query)
    return [user[0] for user in users.fetchall()]


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> UserBase | None:
    result = await db.execute(select(UserBase).where(UserBase.id == user_id))
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found"
        )

    return user


async def create_user(db: AsyncSession, user_data: users.UserSignUp) -> UserBase:
    query = insert(UserBase).values(
        username=user_data.username,
        email=user_data.email,
        password=password_helper.hash_password(user_data.password),
    )
    result = await db.execute(query)
    await db.commit()
    logger.info(f"User {result.inserted_primary_key} has been created")
    return {**user_data.model_dump(), "id": result.inserted_primary_key}


async def update_user(
    db: AsyncSession, user_id: UUID, user_data: users.UserUpdate
) -> UserBase:
    db_user = await get_user_by_id(db, user_id)
    user_data = user_data.model_dump(exclude_unset=True)

    if "password" in user_data:
        user_data["password"] = password_helper.hash_password(user_data["password"])

    query = update(UserBase).where(UserBase.id == user_id).values(**user_data)

    await db.execute(query)
    await db.commit()
    logger.info(f"User {db_user.id} has been updated")
    return db_user


async def delete_user(db: AsyncSession, user_id: UUID) -> dict:
    db_user = await get_user_by_id(db, user_id)

    await db.execute(delete(UserBase).where(UserBase.id == user_id))
    await db.commit()
    logger.info(f"User {db_user.id} has been deleted")
    return {"message": "User has been deleted successfully"}
