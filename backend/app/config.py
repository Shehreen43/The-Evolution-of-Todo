from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    algorithm: str = "HS256"
    jwt_expiration_days: int = 7
    cors_origins: str = "http://localhost:3000"

    # For Phase III AI Chatbot functionality
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: Optional[str] = None
    groq_api_key: Optional[str] = None
    groq_base_url: Optional[str] = None
    default_model: Optional[str] = None
    fallback_model: Optional[str] = None
    fallback_models: Optional[List[str]] = None
    environment: Optional[str] = "development"
    debug: Optional[bool] = True
    max_history_messages: Optional[int] = 50
    log_level: Optional[str] = "INFO"
    frontend_url: Optional[str] = "http://localhost:3000"
    jwt_algorithm: Optional[str] = "HS256"  # Added for compatibility

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()