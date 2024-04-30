from uuid import UUID
from pydantic import BaseModel

from app.db.models import RequestType


class RequestBase(BaseModel):
    request_type: RequestType


class GetRequest(RequestBase):
    id: UUID
    company_id: UUID
    user_id: UUID
