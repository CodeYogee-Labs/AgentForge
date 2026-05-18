"""Configuration helpers for MCP server runtime settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class DbSettings:
    """Container for PostgreSQL connection settings used by MCP tool handlers."""

    host: str
    port: int
    database: str
    user: str
    password: str



def get_db_settings() -> DbSettings:
    """Read database settings from environment variables and return a typed config object."""

    return DbSettings(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv("POSTGRES_DB", "media_rights"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )
