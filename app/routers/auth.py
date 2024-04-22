from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.dependencies import get_db
from app.schemas.auth import Token
from app.schemas.users import UserSignIn, UserSignUp
from app.services.auth import AuthService
from app.utils.auth import authorize_user

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    user_data: UserSignIn,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
) -> Token:
    return await auth_service.sign_in(db=db, user_data=user_data)


@router.get("/me", response_model=UserSignUp, status_code=status.HTTP_200_OK)
async def get_user_account(
    payload: dict = Depends(authorize_user),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
) -> UserSignUp:
    return await auth_service.get_active_user(db=db, payload=payload)
