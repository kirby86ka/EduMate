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
    
    firebase_credentials_path: str = "firebase-credentials.json"
    
    admin_api_key: str = "admin-key-change-in-production"
    ai_api_key: str = "ai-key-change-in-production"
    
    cors_origins: list = ["http://localhost:5000", "http://localhost:3000"]


settings = Settings()
