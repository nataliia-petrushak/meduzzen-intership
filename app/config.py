import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    allowed_origins: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
    ]

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", ".env"
        )

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}"
            f":{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}" f"/{self.REDIS_DB}"


settings = Settings()
