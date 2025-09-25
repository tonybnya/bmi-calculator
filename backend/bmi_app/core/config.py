"""
Script Name : config.py
Description : App settings & environment variables
Author      : @tonybnya
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and configuration.
    """
    # Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # App settings
    app_name: str = "BMI Calculator API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database settings
    database_url: str = "sqlite:///./bmi_calculator.db"

    # Security settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS settings
    allowed_origins_str: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"

    @property
    def allowed_origins(self) -> List[str]:
        """Parse comma-separated origins into a list."""
        return [origin.strip() for origin in self.allowed_origins_str.split(",") if origin.strip()]

    # API settings
    api_v1_prefix: str = "/api/v1"

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000



@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    """
    return Settings()
