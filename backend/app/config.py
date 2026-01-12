from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    algorithm: str = "HS256"
    jwt_expiration_days: int = 7
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()