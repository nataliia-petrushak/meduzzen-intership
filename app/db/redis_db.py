import aioredis
from config import settings


class RedisInit:
    def __init__(self):
        self._pool = aioredis.ConnectionPool.from_url(
            str(settings.REDIS_URL), max_connections=10, decode_responses=True
        )

    async def get_redis_client(self) -> aioredis.Redis:
        return aioredis.Redis(connection_pool=self._pool)

    async def read_from_redis(self, key: str) -> dict:
        async with self.get_redis_client() as redis_client:
            value = await redis_client.get(key)
            if value is not None:
                return {"key": key, "value": value.decode()}
            else:
                return {"message": "Key not found in Redis"}

    async def write_to_redis(self, key: str, value: str) -> dict:
        async with self.get_redis_client() as redis_client:
            await redis_client.set(key, value)
            return {"message": f"Value '{value}' written to Redis with key '{key}'"}
