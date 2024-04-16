from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    LOG_LEVEL: str
    allowed_origins: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
    ]

    class Config:
        env_file = ".env"

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}"
            f":{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}"
            f":{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


settings = Settings()
