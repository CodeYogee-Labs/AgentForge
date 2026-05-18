"""Pydantic request/response models for MCP-style tool invocation endpoints."""

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ToolCallRequest(BaseModel):
    """Represents a generic MCP-like tool call request payload."""

    name: str = Field(..., description="Tool name to execute.")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool input arguments.")


class ToolCallResponse(BaseModel):
    """Represents a generic MCP-like tool call response payload."""

    name: str = Field(..., description="Tool name that was executed.")
    result: Dict[str, Any] = Field(..., description="Structured tool output payload.")


class ToolsListResponse(BaseModel):
    """Represents the list of tools exposed by the MCP server."""

    tools: List[Dict[str, Any]] = Field(..., description="Tool metadata used by orchestration clients.")
