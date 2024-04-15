from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserList(UserBase):
    id: UUID

    class Meta:
        orm_mode = True


class UserDetail(UserList):
    pass


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserSignUp(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str | None
