"""Streamlit chat entrypoint for querying MCP-backed tools through LangChain."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv



def _init_session_state() -> None:
    """Initialize Streamlit session keys used for chat history and service caching."""

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "service" not in st.session_state:
        st.session_state.service = None
    if "troubleshooter" not in st.session_state:
        st.session_state.troubleshooter = None
    if "diag_models_result" not in st.session_state:
        st.session_state.diag_models_result = None
    if "diag_health_result" not in st.session_state:
        st.session_state.diag_health_result = None



def _get_service():
    """Lazy-load and cache agent service instance used to handle chat questions."""

    if st.session_state.service is None:
        from orchestration.agent_service import MediaRightsAgentService

        st.session_state.service = MediaRightsAgentService()
    return st.session_state.service


def _get_troubleshooter():
    """Lazy-load and cache LLM troubleshooter used in the sidebar diagnostics panel."""

    if st.session_state.troubleshooter is None:
        from orchestration.config import get_config
        from orchestration.llm_troubleshooting import LLMTroubleshooter

        st.session_state.troubleshooter = LLMTroubleshooter(get_config())
    return st.session_state.troubleshooter



def _render_sidebar() -> None:
    """Render runtime metadata and help text in Streamlit sidebar."""

    troubleshooter = _get_troubleshooter()
    cfg = troubleshooter.cfg

    st.sidebar.header("Runtime")
    st.sidebar.write(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'ollama')}")
    st.sidebar.write(f"MCP_SERVER_BASE_URL: {os.getenv('MCP_SERVER_BASE_URL', 'http://localhost:8000')}")
    st.sidebar.write(f"LLM_MODEL: {troubleshooter.selected_model()}")

    st.sidebar.header("LLM Troubleshooting")
    if cfg.llm_provider == "gemini":
        st.sidebar.caption("Recommended Gemini models: gemini-2.5-flash, gemini-2.0-flash")

    if st.sidebar.button("Get available models", use_container_width=True):
        st.session_state.diag_models_result = troubleshooter.list_available_models()

    if st.sidebar.button("Health check current model", use_container_width=True):
        st.session_state.diag_health_result = troubleshooter.health_check()

    if st.session_state.diag_models_result is not None:
        with st.sidebar.expander("Available Models", expanded=False):
            st.json(st.session_state.diag_models_result)

    if st.session_state.diag_health_result is not None:
        with st.sidebar.expander("Model Health Check", expanded=False):
            st.json(st.session_state.diag_health_result)

    st.sidebar.header("Example Queries")
    st.sidebar.write("Show details for contract 123")
    st.sidebar.write("Summarize payment schedule for contract 123")
    st.sidebar.write("Provide cost breakdown for contract 123")

    st.sidebar.header("Organization")
    st.sidebar.write(f"Authors: {os.getenv('Authors', 'Prajakt Thale and Krunal Tadwala')}")
    st.sidebar.write(f"Organization: {os.getenv('Organization', 'CodeYogee-Labs (https://github.com/CodeYogee-Labs)')}")



def _render_chat_history() -> None:
    """Render all chat messages from session state in chronological order."""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



def _append_message(role: str, content: str) -> None:
    """Append one chat message to session history."""

    st.session_state.messages.append({"role": role, "content": content})



def main() -> None:
    """Run the Streamlit application lifecycle and process user chat inputs."""

    load_dotenv()
    _init_session_state()

    st.set_page_config(page_title="AgentForge MCP Chat", page_icon="💬", layout="wide")
    st.title("AgentForge MCP Chat")
    st.caption("Streamlit UI + MCP server integration + LangChain orchestration")

    _render_sidebar()
    _render_chat_history()

    user_input = st.chat_input("Ask a question and include an identifier like contract 123")
    if not user_input:
        return

    _append_message("user", user_input)
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        service = _get_service()
        response = service.ask(user_input)
        answer_text = response.answer_text

        _append_message("assistant", answer_text)
        with st.chat_message("assistant"):
            st.markdown(answer_text)

            with st.expander("Execution details"):
                planned = [
                    {"tool_name": c.tool_name, "arguments": c.arguments}
                    for c in response.planned_calls
                ]
                st.json({"planned_calls": planned, "tool_results": response.tool_results})
    except Exception as exc:  # noqa: BLE001
        error_text = f"Error: {exc}"
        _append_message("assistant", error_text)
        with st.chat_message("assistant"):
            st.error(error_text)


if __name__ == "__main__":
    main()
