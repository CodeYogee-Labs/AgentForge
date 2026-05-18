"""Database helpers for opening PostgreSQL connections and executing read-only queries."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Dict, Iterable, Iterator, List

import psycopg
from psycopg.rows import dict_row

from .settings import get_db_settings


@contextmanager
def get_connection() -> Iterator[psycopg.Connection]:
    """Yield a PostgreSQL connection configured from environment variables."""

    cfg = get_db_settings()
    conn = psycopg.connect(
        host=cfg.host,
        port=cfg.port,
        dbname=cfg.database,
        user=cfg.user,
        password=cfg.password,
        row_factory=dict_row,
    )
    try:
        yield conn
    finally:
        conn.close()



def fetch_all(query: str, params: Iterable[Any] | None = None) -> List[Dict[str, Any]]:
    """Execute a SQL query and return all result rows as dictionaries."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
    return [dict(row) for row in rows]



def fetch_one(query: str, params: Iterable[Any] | None = None) -> Dict[str, Any] | None:
    """Execute a SQL query and return the first row as a dictionary when available."""

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            row = cur.fetchone()
    return dict(row) if row else None
