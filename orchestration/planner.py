"""Heuristic query planner that maps user prompts to one or more MCP tool calls."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


CONTRACT_PATTERN = re.compile(r"\bcontract\s*([0-9]+)\b", flags=re.IGNORECASE)


@dataclass(frozen=True)
class PlannedCall:
    """Represents one MCP tool invocation planned for the current user request."""

    tool_name: str
    arguments: Dict[str, str]



def extract_contract_number(user_query: str) -> str | None:
    """Extract contract number from user text when present in the expected phrase format."""

    match = CONTRACT_PATTERN.search(user_query)
    if not match:
        return None
    return match.group(1)



def plan_tool_calls(user_query: str) -> List[PlannedCall]:
    """Generate an ordered tool-call plan based on query intent and contract identifier."""

    contract_number = extract_contract_number(user_query)
    if not contract_number:
        return []

    user_query_lowered = user_query.lower()
    calls: List[PlannedCall] = []

    # Always include titles to provide context in responses.
    calls.append(PlannedCall(tool_name="get_titles_for_contract", arguments={"contract_number": contract_number}))

    if "amort" in user_query_lowered:
        calls.append(
            PlannedCall(tool_name="get_amort_schedule_for_contract", arguments={"contract_number": contract_number})
        )
    if "payment" in user_query_lowered:
        calls.append(
            PlannedCall(tool_name="get_payment_schedule_for_contract", arguments={"contract_number": contract_number})
        )
    if "cost" in user_query_lowered or "license" in user_query_lowered or "subdub" in user_query_lowered:
        calls.append(
            PlannedCall(tool_name="get_cost_breakdown_for_contract", arguments={"contract_number": contract_number})
        )
    if "close" in user_query_lowered or "closing" in user_query_lowered:
        calls.append(PlannedCall(tool_name="get_contract_closing_data", arguments={"contract_number": contract_number}))

    # If only titles were selected, include amort as a useful default for contract summary requests.
    if len(calls) == 1:
        calls.append(
            PlannedCall(tool_name="get_amort_schedule_for_contract", arguments={"contract_number": contract_number})
        )

    return calls
