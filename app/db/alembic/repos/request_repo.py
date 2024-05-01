from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Request, User, Company


class RequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(Request)

    async def request_list(
        self,
        db: AsyncSession,
        request_type: str,
        company_id: UUID = None,
        user_id: UUID = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[User] | list[Company]:
        if company_id:
            query = (
                select(User)
                .join(self.model, self.model.user_id == User.id)
                .where(
                    and_(
                        self.model.company_id == company_id,
                        self.model.request_type == request_type,
                    )
                )
            )
        else:
            query = (
                select(Company)
                .join(self.model, self.model.company_id == Company.id)
                .where(
                    and_(
                        self.model.user_id == user_id,
                        self.model.request_type == request_type,
                    )
                )
            )
        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        return [result[0] for result in result.fetchall()]
