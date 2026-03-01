"""
Configuration settings for the MCP Gmail + Google Calendar server.
"""

import json
import os
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Import default settings from gmail module
from mcp_gmail.gmail import (
    DEFAULT_CREDENTIALS_PATH,
    DEFAULT_TOKEN_PATH,
    DEFAULT_USER_ID,
    GMAIL_SCOPES,
)

# NEW — Add Calendar scopes
try:
    from mcp_gmail.calendar import CALENDAR_SCOPES
except ImportError:
    # fallback if you haven't created mcp_gmail/calendar.py
    CALENDAR_SCOPES = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ]


class Settings(BaseSettings):
    """
    Settings model for MCP Gmail + Calendar server configuration.

    Automatically reads from environment variables with MCP_GMAIL_ prefix.
    """

    credentials_path: str = DEFAULT_CREDENTIALS_PATH
    token_path: str = DEFAULT_TOKEN_PATH

    # ✔ Combine Gmail + Calendar scopes
    scopes: List[str] = GMAIL_SCOPES + CALENDAR_SCOPES

    user_id: str = DEFAULT_USER_ID
    max_results: int = 10

    # Configure environment variable settings
    model_config = SettingsConfigDict(
        env_prefix="MCP_GMAIL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


def get_settings(config_file: Optional[str] = None) -> Settings:
    """
    Get settings instance, optionally loaded from a config file.
    """

    if config_file is None:
        return Settings()

    if config_file and os.path.exists(config_file):
        with open(config_file, "r") as f:
            data = json.load(f)
            return Settings.model_validate(data)

    return Settings()


# Default settings instance
settings = get_settings()
