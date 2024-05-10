from uuid import UUID
from pydantic import BaseModel

from app.db.models import RequestType
from app.schemas.company import GetCompany
from app.schemas.users import GetUser


class RequestBase(BaseModel):
    request_type: RequestType


class GetRequest(RequestBase):
    id: UUID
    company_id: UUID
    user_id: UUID


class CompanyRequest(RequestBase):
    id: UUID
    company: GetCompany


class UserRequest(RequestBase):
    id: UUID
    user: GetUser
