"""Observability helpers for console logging and LangSmith tracing."""

from __future__ import annotations

import logging
import os

from .config import AppConfig


_LOGGING_CONFIGURED = False


def setup_observability(cfg: AppConfig) -> None:
    """Configure process logging and LangSmith environment variables from app config."""

    _configure_console_logging(cfg)
    _configure_langsmith(cfg)


def _configure_console_logging(cfg: AppConfig) -> None:
    """Initialize root console logger once and respect configured log level."""

    global _LOGGING_CONFIGURED

    if not cfg.console_logging_enabled:
        logging.disable(logging.CRITICAL)
        return

    if _LOGGING_CONFIGURED:
        return

    logging.basicConfig(
        level=getattr(logging, cfg.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    _LOGGING_CONFIGURED = True


def _configure_langsmith(cfg: AppConfig) -> None:
    """Set LangSmith env values so LangChain can emit traces when enabled."""

    if not cfg.langsmith_enabled:
        return

    api_key = os.getenv("LANGSMITH_API_KEY", "").strip()
    if not api_key:
        logging.getLogger(__name__).warning(
            "LANGSMITH_ENABLED is true but LANGSMITH_API_KEY is missing; LangSmith tracing is disabled."
        )
        return

    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = api_key
    os.environ["LANGSMITH_PROJECT"] = cfg.langsmith_project

    logging.getLogger(__name__).info("LangSmith tracing enabled for project '%s'.", cfg.langsmith_project)
