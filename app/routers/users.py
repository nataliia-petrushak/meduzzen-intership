from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from dependencies import get_db
from schemas.users import GetUser, UserDetail, UserSignUp, UserUpdate
from crud import users

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=List[GetUser])
async def get_user_list(offset: int, limit: int, db: AsyncSession = Depends(get_db)):
    return await users.get_all_users(db=db, offset=offset, limit=limit)


@router.get("/{user_id}/", response_model=UserDetail)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await users.get_user_by_id(db, user_id=user_id)


@router.post("/", response_model=UserSignUp)
async def create_user(user_data: UserSignUp, db: AsyncSession = Depends(get_db)):
    return await users.create_user(user_data=user_data, db=db)


@router.patch("/{user_id}/", response_model=UserUpdate)
async def update_user(
    user_id: UUID, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    return await users.update_user(user_data=user_data, db=db, user_id=user_id)


@router.delete("/{user_id}/", response_model=dict)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await users.delete_user(user_id=user_id, db=db)
