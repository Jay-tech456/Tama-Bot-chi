from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_username: str = "default"
    redis_password: str = ""
    redis_db: int = 0
    
    # Anthropic Claude (optional for development)
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    claude_model: str = "claude-sonnet-4-20250514"
    
    # Sanity CMS (optional for development)
    sanity_project_id: str = Field(default="", description="Sanity project ID")
    sanity_dataset: str = "production"
    sanity_api_version: str = "2024-01-01"
    sanity_token: str = Field(default="", description="Sanity API token")
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


settings = Settings()
