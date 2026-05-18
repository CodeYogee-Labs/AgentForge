"""Prompt templates used to synthesize final user-facing responses from tool outputs."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate



def build_answer_prompt() -> ChatPromptTemplate:
    """Build the response prompt that constrains the model to tool-grounded answers."""

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a media-rights assistant. Only use tool data provided in context. "
                "If data is missing, clearly say it is unavailable. Keep answers concise, text-first, and easy to read.",
            ),
            (
                "human",
                "User query: {user_query}\n\n"
                "Tool results JSON:\n{tool_results_json}\n\n"
                "Respond with: 1) short summary 2) key details grouped by section 3) totals if available.",
            ),
        ]
    )
