from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator, ValidationError


class UserBase(BaseModel):
    email: EmailStr
    username: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, email: EmailStr) -> EmailStr:
        if len(email) >= 100:
            raise ValidationError("Email is too long")
        return email

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, username: str) -> str:
        if not username or len(username) >= 20:
            raise ValidationError("Username is too long")
        return username


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

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, password: str):
        if len(password) >= 250:
            raise ValidationError("Password is too long")
        if not password or len(password) < 8:
            raise ValidationError("Password is too short")
        return password


class UserUpdate(BaseModel):
    username: str | None
    password: str | None

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, username: str) -> str:
        if username and len(username) >= 20:
            raise ValidationError("Username is too long")
        return username

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, password: str):
        if password:
            if len(password) >= 250:
                raise ValidationError("Password is too long")
            if len(password) < 8:
                raise ValidationError("Password is too short")
        return password
