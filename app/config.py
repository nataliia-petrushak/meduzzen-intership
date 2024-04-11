from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator


class Settings(BaseSettings):
    HOST: str
    PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    REDIS_URL: str
    allowed_origins: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000"
    ]

    class Config:
        env_file = ".env"

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DATABASE_USER}:"
                f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}"
                f":{self.DATABASE_PORT}/{self.DATABASE_NAME}")


settings = Settings()
