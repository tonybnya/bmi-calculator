"""
Script Name : config.py
Description : App settings & environment variables
Author      : @tonybnya
"""
from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Application settings and configuration.
    """
    # App settings
    app_name: str = Field(default="BMI Calculator API", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")

    # Database settings
    database_url: str = Field(
        default="sqlite:///./bmi.db",
        env="DATABASE_URL",
        description="Database connection URL"
    )

    # Security settings
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        env="SECRET_KEY",
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # CORS settings
    allowed_origins: list[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174"
        ],
        env="ALLOWED_ORIGINS"
    )

    # API settings
    api_v1_prefix: str = Field(default="/api/v1", env="API_V1_PREFIX")

    # Server settings
    host: str = Field(default="127.0.0.1", env="HOST")
    port: int = Field(default=8000, env="PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            """Custom parser for environment variables."""
            if field_name == "allowed_origins":
                # Parse comma-separated string into list
                return [origin.strip() for origin in raw_val.split(",") if origin.strip()]
            elif field_name == "debug":
                # Parse boolean values
                return raw_val.lower() in ("true", "1", "yes", "on")
            return raw_val


@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    """
    return Settings()
