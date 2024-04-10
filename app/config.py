from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str
    port: int
    allowed_origins: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000"
    ]

    class Config:
        env_file = [".env_docker", ".env"]


settings = Settings()
