import pickle
from datetime import timedelta
from typing import Any

from redis.asyncio import ConnectionPool, Redis
from app.config import settings


class DBRedisManager:
    def __init__(self):
        self._pool = ConnectionPool.from_url(
            settings.redis_url, max_connections=10, decode_responses=False
        )
        self._redis_client = Redis(connection_pool=self._pool)

    async def get_value(self, key: Any) -> dict:
        if value := await self._redis_client.get(key):
            return {"key": key, "value": pickle.loads(value)}
        return {"message": "Key not found in Redis"}

    async def set_value(self, key: Any, value: Any) -> dict:
        await self._redis_client.set(key, pickle.dumps(value), ex=timedelta(hours=48))
        return {"message": f"Value '{value}' written to Redis with key '{key}'"}
