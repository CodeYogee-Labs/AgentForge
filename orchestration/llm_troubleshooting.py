"""Provider diagnostics helpers for listing models and validating LLM connectivity."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List

import requests

from .config import AppConfig
from .llm_factory import build_chat_model


@dataclass(frozen=True)
class LLMTroubleshooter:
    """Utility wrapper that provides provider-specific model diagnostics."""

    cfg: AppConfig

    def selected_model(self) -> str:
        """Return model name configured for the active provider."""

        provider = self.cfg.llm_provider
        if provider == "openai":
            return self.cfg.openai_model
        if provider == "gemini":
            return self.cfg.gemini_model
        if provider == "groq":
            return self.cfg.groq_model
        if provider == "ollama":
            return self.cfg.ollama_model
        return ""

    def list_available_models(self) -> Dict[str, Any]:
        """List models for the configured provider and include troubleshooting hints."""

        provider = self.cfg.llm_provider
        if provider == "gemini":
            return self._list_gemini_models()
        if provider == "openai":
            return self._list_openai_models()
        if provider == "groq":
            return self._list_groq_models()
        if provider == "ollama":
            return self._list_ollama_models()
        return {
            "status": "error",
            "provider": provider,
            "error": "Unsupported provider for diagnostics",
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform a minimal invocation against the active provider and model."""

        started = time.perf_counter()
        try:
            model = build_chat_model(self.cfg)
            response = model.invoke("Reply with exactly OK")
            latency_ms = int((time.perf_counter() - started) * 1000)
            text = getattr(response, "content", str(response))
            return {
                "status": "ok",
                "provider": self.cfg.llm_provider,
                "model": self.selected_model(),
                "latency_ms": latency_ms,
                "response_preview": str(text)[:200],
            }
        except Exception as exc:  # noqa: BLE001
            message = str(exc)
            return {
                "status": "error",
                "provider": self.cfg.llm_provider,
                "model": self.selected_model(),
                "error": message,
                "hint": self._build_hint(message),
            }

    def recommended_gemini_models(self, available_models: List[str] | None = None) -> List[str]:
        """Return preferred Gemini models, optionally filtered by currently available models."""

        preferred = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash-lite",
        ]
        if not available_models:
            return preferred

        available_set = set(available_models)
        ranked = [model for model in preferred if model in available_set]
        if ranked:
            return ranked
        return sorted(available_models)[:10]

    def _list_openai_models(self) -> Dict[str, Any]:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return self._missing_key_error("OPENAI_API_KEY")

        try:
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=25,
            )
            response.raise_for_status()
            payload = response.json()
            models = sorted(item.get("id") for item in payload.get("data", []) if item.get("id"))
            return {
                "status": "ok",
                "provider": "openai",
                "model_count": len(models),
                "selected_model": self.cfg.openai_model,
                "models": models,
            }
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "provider": "openai", "error": str(exc)}

    def _list_groq_models(self) -> Dict[str, Any]:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return self._missing_key_error("GROQ_API_KEY")

        try:
            response = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=25,
            )
            response.raise_for_status()
            payload = response.json()
            models = sorted(item.get("id") for item in payload.get("data", []) if item.get("id"))
            return {
                "status": "ok",
                "provider": "groq",
                "model_count": len(models),
                "selected_model": self.cfg.groq_model,
                "models": models,
            }
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "provider": "groq", "error": str(exc)}

    def _list_ollama_models(self) -> Dict[str, Any]:
        endpoint = f"{self.cfg.ollama_base_url.rstrip('/')}/api/tags"
        try:
            response = requests.get(endpoint, timeout=15)
            response.raise_for_status()
            payload = response.json()
            models = sorted(item.get("name") for item in payload.get("models", []) if item.get("name"))
            return {
                "status": "ok",
                "provider": "ollama",
                "model_count": len(models),
                "selected_model": self.cfg.ollama_model,
                "models": models,
                "endpoint": endpoint,
            }
        except Exception as exc:  # noqa: BLE001
            return {
                "status": "error",
                "provider": "ollama",
                "endpoint": endpoint,
                "error": str(exc),
            }

    def _list_gemini_models(self) -> Dict[str, Any]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return self._missing_key_error("GEMINI_API_KEY")

        try:
            response = requests.get(
                "https://generativelanguage.googleapis.com/v1beta/models",
                params={"key": api_key},
                timeout=25,
            )
            response.raise_for_status()
            payload = response.json()

            supported: List[str] = []
            all_models: List[Dict[str, Any]] = []
            for item in payload.get("models", []):
                name = item.get("name", "")
                model_id = name.split("/", 1)[1] if name.startswith("models/") else name
                methods = item.get("supportedGenerationMethods", [])
                all_models.append({"id": model_id, "methods": methods})
                if "generateContent" in methods:
                    supported.append(model_id)

            supported.sort()
            selected = self.cfg.gemini_model
            recommendations = self.recommended_gemini_models(supported)
            return {
                "status": "ok",
                "provider": "gemini",
                "model_count": len(supported),
                "selected_model": selected,
                "selected_model_supported": selected in set(supported),
                "models": supported,
                "recommended_models": recommendations,
                "raw_models": all_models,
            }
        except Exception as exc:  # noqa: BLE001
            return {"status": "error", "provider": "gemini", "error": str(exc)}

    def _build_hint(self, message: str) -> str:
        """Build a concise, provider-aware troubleshooting hint from exception text."""

        lowered = message.lower()
        if "notfound" in lowered or "404" in lowered:
            if self.cfg.llm_provider == "gemini":
                return (
                    "Configured Gemini model is unavailable for generateContent. "
                    "Use 'Get available models' and pick one of the recommended Gemini models."
                )
            return "Configured model was not found. Use 'Get available models' and update the model env var."
        if "api key" in lowered or "unauthorized" in lowered or "401" in lowered:
            return "API key is missing or invalid for the selected provider."
        if "connection" in lowered or "timed out" in lowered:
            return "Provider endpoint is unreachable or slow. Verify network access and endpoint URL."
        return "Review provider/model configuration and run model listing before retrying."

    def _missing_key_error(self, env_var_name: str) -> Dict[str, Any]:
        return {
            "status": "error",
            "provider": self.cfg.llm_provider,
            "error": f"{env_var_name} is required for this operation",
        }