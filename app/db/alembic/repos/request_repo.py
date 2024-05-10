from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Request, User, Company


class RequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(Request)
