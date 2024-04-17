from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}"
            f":{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}"
            f":{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"
        )


class TestDatabaseSettings(BaseSettings):
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_NAME: str

    @property
    def test_postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}"
            f":{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}"
            f":{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class AppSettings(BaseSettings):
    HOST: str
    PORT: int
    LOG_LEVEL: str
    allowed_origins: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
    ]
    model_config = SettingsConfigDict(env_file=".env")


class Settings(AppSettings, RedisSettings, PostgresSettings, TestDatabaseSettings):
    pass


settings = Settings(_env_file=".env")
