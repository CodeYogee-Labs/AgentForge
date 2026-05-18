"""HTTP client wrappers for interacting with the local FastAPI MCP server."""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List

import requests


LOGGER = logging.getLogger(__name__)


class MCPClient:
    """Simple MCP-like client that supports listing tools and invoking named tools."""

    def __init__(self, base_url: str, timeout_seconds: int = 600) -> None:
        """Initialize the MCP client with server URL and request timeout."""

        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def health(self) -> Dict[str, Any]:
        """Check server health and return status payload."""

        started_at = time.perf_counter()
        response = requests.get(f"{self.base_url}/health", timeout=self.timeout_seconds)
        response.raise_for_status()
        LOGGER.info("MCP health check succeeded in %.2f ms.", (time.perf_counter() - started_at) * 1000)
        return response.json()

    def list_tools(self) -> List[Dict[str, Any]]:
        """Fetch and return tool metadata from the MCP server."""

        started_at = time.perf_counter()
        response = requests.get(f"{self.base_url}/tools/list", timeout=self.timeout_seconds)
        response.raise_for_status()
        payload = response.json()
        tools = payload.get("tools", [])
        LOGGER.info(
            "Fetched MCP tool catalog (tool_count=%d, duration_ms=%.2f).",
            len(tools),
            (time.perf_counter() - started_at) * 1000,
        )
        return tools

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a named tool with arguments and return the tool result payload."""

        started_at = time.perf_counter()
        response = requests.post(
            f"{self.base_url}/tools/call",
            json={"name": tool_name, "arguments": arguments},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        LOGGER.info(
            "MCP tool call completed (tool=%s, duration_ms=%.2f).",
            tool_name,
            (time.perf_counter() - started_at) * 1000,
        )
        return payload.get("result", {})
