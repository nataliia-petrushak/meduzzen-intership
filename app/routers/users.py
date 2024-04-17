from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas.users import GetUser, UserDetail, UserSignUp, UserUpdate
from services.users import user_services

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=List[GetUser])
async def get_user_list(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await user_services.get_model_list(db, offset=offset, limit=limit)


@router.get("/{user_id}/", response_model=UserDetail)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await user_services.get_model_by_id(db, model_id=user_id)


@router.post("/", response_model=UserSignUp)
async def create_user(user_data: UserSignUp, db: AsyncSession = Depends(get_db)):
    return await user_services.create_model(model_data=user_data, db=db)


@router.patch("/{user_id}/", response_model=UserUpdate)
async def update_user(
    user_id: UUID, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    return await user_services.update_model(
        model_data=user_data, db=db, model_id=user_id
    )


@router.delete("/{user_id}/", response_model=dict)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await user_services.delete_model(model_id=user_id, db=db)
