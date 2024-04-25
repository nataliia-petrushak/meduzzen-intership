from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.database import get_db
from app.dependencies import check_permissions
from app.schemas.users import GetUser, UserDetail, UserUpdate
from app.services.auth import get_authenticated_user
from app.services.user import UserService


router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=list[GetUser], status_code=status.HTTP_200_OK)
async def get_user_list(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
) -> list[GetUser]:
    return await user_service.get_model_list(db=db, offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserDetail, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
) -> UserDetail:
    return await user_service.get_model_by_id(db=db, model_id=user_id)


@router.patch("/{user_id}", response_model=UserUpdate, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
) -> UserUpdate:
    await check_permissions(user_id=user_id, user=user)
    return await user_service.update_model(
            model_data=user_data, db=db, model_id=user_id
        )


@router.patch("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: UUID,
    user: GetUser = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
) -> None:
    await check_permissions(user_id=user_id, user=user)
    return await user_service.user_deactivate(user_id=user_id, db=db)
