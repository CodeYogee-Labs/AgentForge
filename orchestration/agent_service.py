"""Application service that orchestrates planning, MCP calls, and LLM response generation."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List

from .config import get_config
from .llm_factory import build_chat_model
from .mcp_client import MCPClient
from .observability import setup_observability
from .planner import PlannedCall, plan_tool_calls
from .planner_automated import plan_tool_calls_with_llm
from .prompts import build_answer_prompt


LOGGER = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Represents the final answer text plus execution details used for debugging and transparency."""

    answer_text: str
    planned_calls: List[PlannedCall]
    tool_results: Dict[str, Any]


class MediaRightsAgentService:
    """Coordinates planning, tool retrieval, and LLM generation for user queries."""

    def __init__(self) -> None:
        """Initialize configuration, MCP client, response prompt, and selected chat model."""

        self.cfg = get_config()
        setup_observability(self.cfg)
        self.mcp_client = MCPClient(base_url=self.cfg.mcp_server_base_url)
        self.prompt = build_answer_prompt()
        self.model = build_chat_model(self.cfg)
        LOGGER.info(
            "Agent service initialized (provider=%s, mcp_base_url=%s, langsmith_enabled=%s)",
            self.cfg.llm_provider,
            self.cfg.mcp_server_base_url,
            self.cfg.langsmith_enabled,
        )

    def _execute_plan(self, calls: List[PlannedCall]) -> Dict[str, Any]:
        """Execute each planned MCP call in order and aggregate responses by tool name."""

        result: Dict[str, Any] = {}
        for call in calls:
            LOGGER.info("Calling MCP tool '%s' with args=%s", call.tool_name, call.arguments)
            payload = self.mcp_client.call_tool(call.tool_name, call.arguments)
            if call.tool_name in result:
                result[call.tool_name].append(payload)
            else:
                result[call.tool_name] = [payload]
        return result

    def _plan_calls(self, user_query: str) -> List[PlannedCall]:
        """Plan calls via LLM from runtime tool metadata, with heuristic fallback for resiliency."""

        try:
            available_tools = self.mcp_client.list_tools()
            planned_calls = plan_tool_calls_with_llm(user_query, available_tools, self.model)
            if planned_calls:
                LOGGER.info("LLM planner selected %d tool call(s).", len(planned_calls))
                return planned_calls
        except Exception as ex:  # noqa: BLE001
            LOGGER.warning("LLM planner failed; falling back to heuristic planner. error=%s", ex)

        fallback_calls = plan_tool_calls(user_query)
        LOGGER.info("Fallback planner selected %d tool call(s).", len(fallback_calls))
        return fallback_calls

    def _fallback_response(self, user_query: str) -> str:
        """Return deterministic guidance when the query lacks a usable identifier."""

        return (
            "I could not identify a usable record identifier in your request. "
            "Please ask with an explicit identifier, for example: contract 123. "
            f"Received query: {user_query}"
        )

    def ask(self, user_query: str) -> AgentResponse:
        """Handle one user query from planning through tool execution and answer synthesis."""

        started_at = time.perf_counter()
        LOGGER.info("Received user query (chars=%d).", len(user_query or ""))

        planned_calls = self._plan_calls(user_query)
        if not planned_calls:
            LOGGER.info("No tool calls were planned; returning deterministic fallback response.")
            return AgentResponse(answer_text=self._fallback_response(user_query), planned_calls=[], tool_results={})

        tool_results = self._execute_plan(planned_calls)
        tool_results_json = json.dumps(tool_results, default=str, indent=2)

        chain = self.prompt | self.model
        llm_result = chain.invoke({"user_query": user_query, "tool_results_json": tool_results_json})

        answer_text = getattr(llm_result, "content", str(llm_result))
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        LOGGER.info(
            "Query handled successfully (planned_calls=%d, duration_ms=%s).",
            len(planned_calls),
            duration_ms,
        )
        return AgentResponse(answer_text=answer_text, planned_calls=planned_calls, tool_results=tool_results)
