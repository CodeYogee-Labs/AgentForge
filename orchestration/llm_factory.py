"""Factory methods for creating LangChain chat model instances from selected providers."""

from __future__ import annotations

import os

from langchain_core.language_models.chat_models import BaseChatModel

from .config import AppConfig



def _create_openai_model(cfg: AppConfig) -> BaseChatModel:
    """Create an OpenAI chat model configured for local orchestration usage."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=cfg.openai_model, temperature=cfg.llm_temperature, api_key=api_key)



def _create_gemini_model(cfg: AppConfig) -> BaseChatModel:
    """Create a Gemini chat model configured for local orchestration usage."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=cfg.gemini_model, temperature=cfg.llm_temperature, google_api_key=api_key)



def _create_groq_model(cfg: AppConfig) -> BaseChatModel:
    """Create a Groq chat model configured for local orchestration usage."""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is required when LLM_PROVIDER=groq")

    from langchain_groq import ChatGroq

    return ChatGroq(model=cfg.groq_model, temperature=cfg.llm_temperature, api_key=api_key)



def _create_ollama_model(cfg: AppConfig) -> BaseChatModel:
    """Create an Ollama chat model targeting a local or remote Ollama endpoint."""

    from langchain_ollama import ChatOllama

    return ChatOllama(model=cfg.ollama_model, base_url=cfg.ollama_base_url, temperature=cfg.llm_temperature)



def build_chat_model(cfg: AppConfig) -> BaseChatModel:
    """Build a provider-specific LangChain chat model based on the configured provider name."""

    provider = cfg.llm_provider
    if provider == "openai":
        return _create_openai_model(cfg)
    if provider == "gemini":
        return _create_gemini_model(cfg)
    if provider == "groq":
        return _create_groq_model(cfg)
    if provider == "ollama":
        return _create_ollama_model(cfg)
    raise ValueError("Unsupported LLM_PROVIDER. Use one of: gemini, openai, groq, ollama")
