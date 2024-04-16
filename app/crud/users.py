from typing import List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger
from db.models import UserBase
from schemas import users
from services.security import password_helper
from starlette import status


async def get_user_list(db: AsyncSession, offset: int, limit: int) -> List[UserBase]:
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
    db_user = UserBase(
        username=user_data.username,
        email=user_data.email,
        password=password_helper.hash_password(user_data.password),
    )
    db.add(db_user)
    await db.commit()
    logger.info(f"User {db_user.id} has been created")
    return db_user


async def update_user(
    db: AsyncSession, user_id: UUID, user_data: users.UserUpdate
) -> UserBase:
    db_user = await get_user_by_id(db, user_id)
    user_data = user_data.dict(exclude_unset=True)

    if "password" in user_data:
        user_data["password"] = password_helper.hash_password(user_data["password"])

    for key, value in user_data.items():
        setattr(db_user, key, value)

    await db.commit()
    logger.info(f"User {db_user.id} has been updated")
    return db_user


async def delete_user(db: AsyncSession, user_id: UUID) -> dict:
    db_user = await get_user_by_id(db, user_id)

    await db.delete(db_user)
    await db.commit()
    logger.info(f"User {db_user.id} has been deleted")
    return {"message": "User has been deleted successfully"}
