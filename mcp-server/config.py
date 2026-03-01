"""
Configuration management for MCP Server.
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """MCP Server configuration."""

    # Sanity Configuration
    SANITY_PROJECT_ID: str = os.getenv("SANITY_PROJECT_ID", "c0j8rp13")
    SANITY_DATASET: str = os.getenv("SANITY_DATASET", "production")
    SANITY_API_TOKEN: Optional[str] = os.getenv("SANITY_API_TOKEN")
    SANITY_API_VERSION: str = os.getenv("SANITY_API_VERSION", "2024-01-01")

    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_USERNAME: Optional[str] = os.getenv("REDIS_USERNAME")

    # SQLite Configuration
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "./data/tama.db")

    # Server Configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "5002"))

    # Caching
    CONVERSATION_CACHE_TTL: int = int(os.getenv("CONVERSATION_CACHE_TTL", "86400"))  # 24 hours
    PROFILE_CACHE_TTL: int = int(os.getenv("PROFILE_CACHE_TTL", "3600"))  # 1 hour
