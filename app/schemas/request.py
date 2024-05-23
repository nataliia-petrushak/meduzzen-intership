from uuid import UUID
from pydantic import BaseModel

from app.schemas.company import GetCompany
from app.schemas.users import GetUser


class RequestBase(BaseModel):
    id: UUID


class GetRequest(RequestBase):
    company_id: UUID
    user_id: UUID


class CompanyRequest(RequestBase):
    company: GetCompany


class UserRequest(RequestBase):
    user: GetUser
