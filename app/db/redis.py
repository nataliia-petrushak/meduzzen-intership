from redis.asyncio import ConnectionPool, Redis
from config import settings


class DBRedisManager:
    def __init__(self):
        self._pool = ConnectionPool.from_url(
            settings.redis_url, max_connections=10, decode_responses=True
        )
        self._redis_client = Redis(connection_pool=self._pool)

    async def get_value(self, key: str) -> dict:
        if value := await self._redis_client.get(key):
            return {"key": key, "value": value.decode()}
        return {"message": "Key not found in Redis"}

    async def set_value(self, key: str, value: str) -> dict:
        await self._redis_client.set(key, value)
        return {"message": f"Value '{value}' written to Redis with key '{key}'"}
