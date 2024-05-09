from datetime import datetime, timedelta

from sqlalchemy import select, func, cast, DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alembic.repos.base_repo import BaseRepository
from app.db.models import QuizResult, User
from app.schemas.quiz_result import AllQuizResults


class QuizResultRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(QuizResult)

    async def get_results_records(
        self, db: AsyncSession, filters: dict
    ) -> list[AllQuizResults]:
        query = select(func.jsonb_array_elements(self.model.all_results)).filter_by(
            **filters
        )
        models = await db.execute(query)
        return [model[0] for model in models.fetchall()]

    async def get_overdue_quiz_results(self, db: AsyncSession):
        date_to_datetime = cast(
            func.jsonb_extract_path_text(self.model.all_results[-1], "date"),
            DateTime(timezone=True),
        )
        query = (
            select(self.model.quiz_id, self.model.user_id, User.email)
            .join(User, self.model.user_id == User.id)
            .filter(date_to_datetime + timedelta(days=2) < datetime.utcnow())
        )
        results = await db.execute(query)
        return results.fetchall()
