import redis
from config import settings


class DBRedisManager:
    def __init__(self):
        self._pool = redis.ConnectionPool.from_url(
            str(settings.REDIS_URL), max_connections=10, decode_responses=True
        )
        self._redis_client = redis.Redis(connection_pool=self._pool)

    async def read_from_redis(self, key: str) -> dict:
        value = await self._redis_client.get(key)
        if value is not None:
            return {"key": key, "value": value.decode()}
        else:
            return {"message": "Key not found in Redis"}

    async def write_to_redis(self, key: str, value: str) -> dict:
        await self._redis_client.set(key, value)
        return {"message": f"Value '{value}' written to Redis with key '{key}'"}
