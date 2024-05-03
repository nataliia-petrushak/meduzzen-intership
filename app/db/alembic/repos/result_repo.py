from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import Result


class ResultRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Result)

    @staticmethod
    async def get_user_results_records(
            db: AsyncSession, param: str, user_id: UUID, company_id: UUID = None
    ) -> list[int]:

        query = (f"SELECT CAST(jsonb_array_elements(all_results)->>'{param}' AS INTEGER) "
                 f"FROM result WHERE user_id = '{str(user_id)}'")
        if company_id:
            query += f" AND company_id = '{str(company_id)}'"
        models = await db.execute(text(query))
        return [model[0] for model in models.fetchall()]
