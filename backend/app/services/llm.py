import asyncio
import logging
from typing import Any
# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
# pyrefly: ignore [missing-import]
from google.genai.errors import APIError

from app.config import settings

logger = logging.getLogger("blind_spot.llm")


class LLMProviderError(Exception):
    """Raised when an LLM provider request fails or encounters an unrecoverable error."""
    pass


class GeminiService:
    """
    Lightweight, provider-specific wrapper for Gemini API calls.
    Handles configuration, timeouts, token capping, and structured JSON output requests.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ):
        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        self._client: genai.Client | None = None
        self._cached_key: str | None = None

    @property
    def timeout(self) -> float:
        return self._timeout or settings.GEMINI_TIMEOUT_SECONDS

    @property
    def api_key(self) -> str:
        return self._api_key or settings.GEMINI_API_KEY

    @property
    def model(self) -> str:
        return self._model or settings.GEMINI_MODEL

    @property
    def client(self) -> genai.Client:
        key = self.api_key
        if not key:
            raise LLMProviderError("GEMINI_API_KEY is not configured on the server.")
        if self._client is None or self._cached_key != key:
            self._client = genai.Client(api_key=key)
            self._cached_key = key
        return self._client

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        """
        Sends system and user prompts to Gemini requesting JSON structured response.
        Enforces timeout and token limits.
        """
        target_temperature = (
            temperature if temperature is not None else settings.GEMINI_TEMPERATURE
        )
        target_tokens = (
            max_output_tokens
            if max_output_tokens is not None
            else settings.GEMINI_MAX_OUTPUT_TOKENS
        )

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=target_temperature,
            max_output_tokens=target_tokens,
        )

        try:
            # Enforce timeout via asyncio.wait_for
            response = await asyncio.wait_for(
                self.client.aio.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=config,
                ),
                timeout=self.timeout,
            )

            text_output = response.text
            if not text_output:
                raise LLMProviderError("Received empty response text from Gemini provider.")

            return text_output

        except asyncio.TimeoutError as exc:
            logger.warning("Gemini request timed out after %.1f seconds", self.timeout)
            raise LLMProviderError(f"Request to Gemini timed out after {self.timeout}s.") from exc
        except APIError as exc:
            # Log safe metadata without exposing API keys or user data
            logger.error("Gemini API error occurred (code: %s)", getattr(exc, "code", "unknown"))
            raise LLMProviderError(f"Gemini API error: {exc.message if hasattr(exc, 'message') else str(exc)}") from exc
        except LLMProviderError:
            raise
        except Exception as exc:
            logger.error("Unexpected error during Gemini API call: %s", type(exc).__name__)
            raise LLMProviderError("Internal error communicating with AI provider.") from exc


# Default global instance for reuse
gemini_service = GeminiService()
