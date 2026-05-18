"""LLM-driven planner that selects MCP tools and argument values from plain-English queries."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from .planner import PlannedCall


_JSON_BLOCK_PATTERN = re.compile(r"\{[\s\S]*\}")



def _build_planner_prompt() -> ChatPromptTemplate:
    """Create a prompt that forces strict JSON planning output from tool metadata."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a tool planner. "
                "Given a user request and available tools, decide which tools to call and with what arguments. "
                "Return JSON only. No markdown, no explanation, no extra text.",
            ),
            (
                "human",
                "User query:\n{user_query}\n\n"
                "Available tools JSON:\n{available_tools_json}\n\n"
                "Return valid JSON with this schema exactly:\n"
                "{{\n"
                "  \"calls\": [\n"
                "    {{\n"
                "      \"tool_name\": \"<tool name from list>\",\n"
                "      \"arguments\": {{\"<arg_name>\": \"<arg_value>\"}}\n"
                "    }}\n"
                "  ]\n"
                "}}\n\n"
                "Rules:\n"
                "1) Only use tool names present in available tools list.\n"
                "2) Infer argument values directly from user query when possible (for example contract numbers, titles).\n"
                "3) If required values are missing, return {{\"calls\": []}}.\n"
                "4) If multiple tools are needed, order them logically.\n"
                "5) Do not invent argument keys not listed in tool metadata.",
            ),
        ]
    )



def _extract_json_object(raw_text: str) -> Dict[str, Any]:
    """Parse planner output into a JSON object, tolerating minor wrapping noise."""

    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json\n", "", 1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = _JSON_BLOCK_PATTERN.search(text)
        if not match:
            return {}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}



def _normalize_content(raw_content: Any) -> str:
    """Convert provider-specific chat message content into plain text."""

    if isinstance(raw_content, str):
        return raw_content

    if isinstance(raw_content, list):
        chunks: List[str] = []
        for item in raw_content:
            if isinstance(item, str):
                chunks.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    chunks.append(text)
        return "\n".join(chunks)

    return str(raw_content)



def _sanitize_calls(raw_calls: Any, available_tools: List[Dict[str, Any]]) -> List[PlannedCall]:
    """Keep only valid tool calls and filter arguments to advertised tool schemas."""

    if not isinstance(raw_calls, list):
        return []

    metadata_by_name: Dict[str, Dict[str, Any]] = {
        str(tool.get("name")): tool for tool in available_tools if tool.get("name")
    }

    planned_calls: List[PlannedCall] = []
    for item in raw_calls:
        if not isinstance(item, dict):
            continue

        tool_name = item.get("tool_name")
        if not isinstance(tool_name, str):
            continue

        tool_meta = metadata_by_name.get(tool_name)
        if tool_meta is None:
            continue

        provided_args = item.get("arguments", {})
        if not isinstance(provided_args, dict):
            provided_args = {}

        allowed_arg_names = set((tool_meta.get("arguments") or {}).keys())
        filtered_args: Dict[str, str] = {}
        for key, value in provided_args.items():
            if key in allowed_arg_names and value is not None:
                filtered_args[str(key)] = str(value)

        required_arg_names = allowed_arg_names
        if any(arg_name not in filtered_args or not filtered_args[arg_name].strip() for arg_name in required_arg_names):
            continue

        planned_calls.append(PlannedCall(tool_name=tool_name, arguments=filtered_args))

    return planned_calls



def plan_tool_calls_with_llm(
    user_query: str,
    available_tools: List[Dict[str, Any]],
    model: BaseChatModel,
) -> List[PlannedCall]:
    """Plan tool calls using an LLM and runtime MCP tool metadata."""

    if not user_query.strip() or not available_tools:
        return []

    prompt = _build_planner_prompt()
    chain = prompt | model
    raw_result = chain.invoke(
        {
            "user_query": user_query,
            "available_tools_json": json.dumps(available_tools, default=str, indent=2),
        }
    )

    content = _normalize_content(getattr(raw_result, "content", raw_result))
    payload = _extract_json_object(content)

    return _sanitize_calls(payload.get("calls"), available_tools)
