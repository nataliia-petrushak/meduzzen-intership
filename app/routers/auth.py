from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.dependencies import get_db
from app.schemas.auth import Token
from app.schemas.users import UserSignIn, GetUser, UserSignUp
from app.services.auth import AuthService, get_authenticated_user

from app.services.user import UserService

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/register", response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserSignUp,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
) -> GetUser:
    return await user_service.create_model(db=db, model_data=user_data)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    user_data: UserSignIn,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
) -> Token:
    return await auth_service.sign_in(db=db, user_data=user_data)


@router.get("/me", response_model=GetUser, status_code=status.HTTP_200_OK)
async def get_user_account(
    user: GetUser = Depends(get_authenticated_user)
) -> GetUser:
    return user
