"""Business logic for media-rights MCP tools backed by PostgreSQL queries."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List

from .db import fetch_all, fetch_one



def _to_json_value(value: Any) -> Any:
    """Convert database-native values (for example Decimal) into JSON-safe primitives."""

    if isinstance(value, Decimal):
        return float(value)
    return value



def _normalize_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize result rows so they can be serialized in JSON responses."""

    return [{k: _to_json_value(v) for k, v in row.items()} for row in rows]



def get_titles_for_contract(contract_number: str) -> Dict[str, Any]:
    """Return all title records associated with a contract number."""

    query = """
        SELECT
            c.contract_number,
            t.id AS title_id,
            t.title_name,
            t.content_type,
            t.season_number,
            t.episode_number,
            t.genre,
            t.duration_minutes,
            ct.territory,
            ct.language_rights,
            ct.platform_rights
        FROM contract c
        JOIN contract_title ct ON c.id = ct.contract_id
        JOIN title t ON t.id = ct.title_id
        WHERE c.contract_number = %s
        ORDER BY t.id;
    """
    rows = fetch_all(query, (contract_number,))
    return {"contract_number": contract_number, "titles": _normalize_rows(rows), "count": len(rows)}



def get_amort_schedule_for_contract(contract_number: str) -> Dict[str, Any]:
    """Return amortization periods for a contract, including optional title metadata."""

    query = """
        SELECT
            c.contract_number,
            ac.period_start,
            ac.period_end,
            ac.title_id,
            t.title_name,
            ac.amort_amount,
            ac.basis,
            ac.notes
        FROM contract c
        JOIN amort_curve ac ON c.id = ac.contract_id
        LEFT JOIN title t ON ac.title_id = t.id
        WHERE c.contract_number = %s
        ORDER BY ac.period_start;
    """
    rows = fetch_all(query, (contract_number,))
    total_amort = sum(row.get("amort_amount") or 0 for row in rows)
    return {
        "contract_number": contract_number,
        "amort_schedule": _normalize_rows(rows),
        "total_amort_amount": _to_json_value(total_amort),
        "count": len(rows),
    }



def get_cost_breakdown_for_contract(contract_number: str) -> Dict[str, Any]:
    """Return aggregated contract cost grouped by cost type."""

    query = """
        SELECT
            c.contract_number,
            cc.cost_type,
            SUM(cc.amount) AS total_amount,
            MAX(cc.currency) AS currency
        FROM contract c
        JOIN contract_cost cc ON c.id = cc.contract_id
        WHERE c.contract_number = %s
        GROUP BY c.contract_number, cc.cost_type
        ORDER BY cc.cost_type;
    """
    rows = fetch_all(query, (contract_number,))
    return {"contract_number": contract_number, "cost_breakdown": _normalize_rows(rows), "count": len(rows)}



def get_payment_schedule_for_contract(contract_number: str) -> Dict[str, Any]:
    """Return payment milestones and statuses for a contract."""

    query = """
        SELECT
            c.contract_number,
            ps.due_date,
            ps.amount,
            ps.currency,
            ps.milestone,
            ps.status
        FROM contract c
        JOIN payment_schedule ps ON c.id = ps.contract_id
        WHERE c.contract_number = %s
        ORDER BY ps.due_date;
    """
    rows = fetch_all(query, (contract_number,))
    return {"contract_number": contract_number, "payment_schedule": _normalize_rows(rows), "count": len(rows)}



def get_contract_closing_data(contract_number: str) -> Dict[str, Any]:
    """Return closing metadata for a contract, if the contract has been closed."""

    query = """
        SELECT
            c.contract_number,
            cd.close_date,
            cd.close_reason,
            cd.final_amort_amount,
            cd.remarks
        FROM contract c
        JOIN closing_data cd ON c.id = cd.contract_id
        WHERE c.contract_number = %s;
    """
    row = fetch_one(query, (contract_number,))
    return {
        "contract_number": contract_number,
        "closing_data": _normalize_rows([row])[0] if row else None,
        "found": bool(row),
    }



def get_contract_exists(contract_number: str) -> bool:
    """Check whether a contract exists for a given contract number."""

    row = fetch_one("SELECT id FROM contract WHERE contract_number = %s", (contract_number,))
    return row is not None
