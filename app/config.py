import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
    app_name: str = "Adaptive Learning API"
    app_version: str = "1.0.0"
    
    mongodb_url: Optional[str] = None
    mongodb_db_name: str = "adaptive_learning"
    use_in_memory: bool = True
    
    admin_api_key: str = "admin-key-change-in-production"
    ai_api_key: str = "ai-key-change-in-production"
    
    cors_origins: list = ["http://localhost:3000"]


settings = Settings()
