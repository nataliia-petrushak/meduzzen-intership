from uuid import UUID
from pydantic import BaseModel

from app.schemas.users import GetUser


class CompanyBase(BaseModel):
    name: str
    description: str
    is_hidden: bool


class GetCompany(CompanyBase):
    id: UUID
    owner_id: UUID


class CompanyDetail(CompanyBase):
    id: UUID
    owner: GetUser


class CompanyCreate(BaseModel):
    name: str
    description: str
    is_hidden: bool


class CompanyUpdate(CompanyBase):
    pass
