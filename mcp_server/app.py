"""FastAPI application that exposes MCP-style tool listing and invocation endpoints."""

from __future__ import annotations

from typing import Any, Callable, Dict

from fastapi import FastAPI, HTTPException

from .schemas import ToolCallRequest, ToolCallResponse, ToolsListResponse
from .services import (
    get_amort_schedule_for_contract,
    get_contract_closing_data,
    get_contract_exists,
    get_cost_breakdown_for_contract,
    get_payment_schedule_for_contract,
    get_titles_for_contract,
)

app = FastAPI(title="Local Media Rights MCP Server", version="1.0.0")


TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "get_titles_for_contract": {
        "description": "Get titles mapped to a contract number.",
        "arguments": {"contract_number": "string"},
        "handler": get_titles_for_contract,
    },
    "get_amort_schedule_for_contract": {
        "description": "Get amortization schedule entries for a contract number.",
        "arguments": {"contract_number": "string"},
        "handler": get_amort_schedule_for_contract,
    },
    "get_cost_breakdown_for_contract": {
        "description": "Get license/subdub/other costs grouped by cost type.",
        "arguments": {"contract_number": "string"},
        "handler": get_cost_breakdown_for_contract,
    },
    "get_payment_schedule_for_contract": {
        "description": "Get payment schedule milestones and statuses for a contract.",
        "arguments": {"contract_number": "string"},
        "handler": get_payment_schedule_for_contract,
    },
    "get_contract_closing_data": {
        "description": "Get contract close date, reason, and final amort amount when available.",
        "arguments": {"contract_number": "string"},
        "handler": get_contract_closing_data,
    },
}



def _get_handler(tool_name: str) -> Callable[[str], Dict[str, Any]]:
    """Resolve a registered tool name into its callable handler."""

    if tool_name not in TOOL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_name}")
    return TOOL_REGISTRY[tool_name]["handler"]


@app.get("/health")
def health() -> Dict[str, str]:
    """Return service health status for readiness checks."""

    return {"status": "ok"}


@app.get("/tools/list", response_model=ToolsListResponse)
def tools_list() -> ToolsListResponse:
    """Return metadata for all tools exposed by the local MCP server."""

    tool_items = [
        {
            "name": name,
            "description": meta["description"],
            "arguments": meta["arguments"],
        }
        for name, meta in TOOL_REGISTRY.items()
    ]
    return ToolsListResponse(tools=tool_items)


@app.post("/tools/call", response_model=ToolCallResponse)
def tools_call(payload: ToolCallRequest) -> ToolCallResponse:
    """Execute a named tool with validated arguments and return structured output."""

    contract_number = payload.arguments.get("contract_number")
    if not contract_number:
        raise HTTPException(status_code=400, detail="Missing required argument: contract_number")

    handler = _get_handler(payload.name)

    if not get_contract_exists(str(contract_number)):
        return ToolCallResponse(
            name=payload.name,
            result={
                "contract_number": str(contract_number),
                "error": "Contract not found",
                "found": False,
            },
        )

    try:
        result = handler(str(contract_number))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {exc}") from exc

    return ToolCallResponse(name=payload.name, result=result)
