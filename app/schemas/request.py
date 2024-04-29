from uuid import UUID
from pydantic import BaseModel

from app.db.models import Status


class RequestBase(BaseModel):
    status: Status


class GetRequest(RequestBase):
    id: UUID
    company_id: UUID
    user_id: UUID
