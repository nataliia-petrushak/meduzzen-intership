from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserSignUp(UserBase):
    password: str


class UserUpdate(UserSignUp):
    pass


class UserSignIn(BaseModel):
    email: str
    password: str


class UserList(UserBase):
    id: int

    class Meta:
        orm_mode = True


class UserDetail(UserList):
    pass
