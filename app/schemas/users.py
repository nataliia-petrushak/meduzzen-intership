from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    email: str
    username: str


class UserList(UserBase):
    class Meta:
        orm_mode = True


class UserDetail(UserBase):
    first_name: str
    last_name: str


class UserSignIn(BaseModel):
    email: str
    password: str


class UserSignUp(UserSignIn):
    username: str
    first_name: str
    last_name: str


class UserUpdate(UserSignUp):
    pass
