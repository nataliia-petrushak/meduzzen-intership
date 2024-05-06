from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import QuizResult


class QuizResultRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(QuizResult)

    async def get_user_results_records(
            self, db: AsyncSession, param: str, filters: dict
    ) -> list[int]:
        query = select(func.jsonb_array_elements(self.model.all_results)).filter_by(**filters)
        models = await db.execute(query)
        return [model[0][param] for model in models.fetchall()]
