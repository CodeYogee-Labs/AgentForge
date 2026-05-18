"""Configuration helpers for orchestration runtime and LLM provider settings."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Typed configuration for selecting LLM provider and MCP server endpoint and other runtime settings."""

    llm_provider: str
    llm_temperature: float
    mcp_server_base_url: str
    openai_model: str
    gemini_model: str
    groq_model: str
    ollama_model: str
    ollama_base_url: str
    console_logging_enabled: bool
    log_level: str
    langsmith_enabled: bool
    langsmith_project: str



def get_config() -> AppConfig:
    """Read environment variables and return normalized application configuration."""

    def _as_bool(raw: str | None, default: bool = False) -> bool:
        if raw is None:
            return default
        return raw.strip().lower() in {"1", "true", "yes", "on"}

    return AppConfig(
        llm_provider=os.getenv("LLM_PROVIDER", "ollama").strip().lower(),
        llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0")),
        mcp_server_base_url=os.getenv("MCP_SERVER_BASE_URL", "http://localhost:8000").rstrip("/"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        console_logging_enabled=_as_bool(os.getenv("CONSOLE_LOGGING_ENABLED", "true"), default=True),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
        langsmith_enabled=_as_bool(os.getenv("LANGSMITH_ENABLED", "false"), default=False),
        langsmith_project=os.getenv("LANGSMITH_PROJECT", "aws-helper-bot-local").strip(),
    )
