from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class GetUser(UserBase):
    id: UUID
    is_active: bool


class UserDetail(GetUser):
    pass


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserSignUp(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None
    password: str | None
