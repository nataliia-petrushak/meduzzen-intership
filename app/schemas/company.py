from uuid import UUID
from pydantic import BaseModel, field_validator, ValidationError

from app.schemas.users import GetUser


class CompanyBase(BaseModel):
    name: str
    description: str

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if len(name) >= 100:
            raise ValidationError("Company name is too long")
        if not name:
            raise ValidationError("Company must have a name")
        return name


class GetCompany(CompanyBase):
    id: UUID
    owner_id: UUID


class CompanyDetail(CompanyBase):
    id: UUID
    owner: GetUser


class CompanyCreate(BaseModel):
    name: str
    description: str

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if len(name) >= 100:
            raise ValidationError("Company name is too long")
        if not name:
            raise ValidationError("Company must have a name")
        return name


class CompanyUpdate(CompanyBase):
    is_hidden: bool = False
