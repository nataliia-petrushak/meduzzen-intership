import csv
from typing import Any

from starlette.responses import StreamingResponse

from app.db.redis import DBRedisManager
from app.schemas.quiz import GetQuiz
from app.schemas.quiz_result import Answers
from app.schemas.users import GetUser


class RedisService:
    def __init__(self) -> None:
        self._redis = DBRedisManager()

    async def get_data_from_redis(self, key: Any) -> list[dict]:
        return await self._redis.get_by_part_of_key(key)

    async def redis_update_or_create_result(self, user: GetUser, quiz: GetQuiz, answers: list[Answers]) -> None:
        result = await self._redis.get_value(f"{quiz.company.id}, {quiz.id}, {user.id}")
        if result:
            result["value"]["answers"].extend(answers)
            await self._redis.set_value(**result)
        else:
            redis_data = {
                "user_id": user.id,
                "company_id": quiz.company_id,
                "quiz_id": quiz.id,
                "answers": answers
            }
            await self._redis.set_value(f"{quiz.company.id}, {quiz.id}, {user.id}", redis_data)

    @staticmethod
    async def data_to_csv(data: list[dict], filename: str):
        headers = list(data[0].keys())
        with open(filename, "w+") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
            yield file.read()

    async def export_csv(self, data: list[dict], filename: str):
        file = self.data_to_csv(data, filename)
        response = StreamingResponse(
            file,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        return response
