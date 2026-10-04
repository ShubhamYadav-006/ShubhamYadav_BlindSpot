import logging
from typing import Optional

from app.prompts.extractor import (
    EXTRACTOR_SYSTEM_PROMPT,
    build_extractor_user_prompt,
)
from app.schemas.response import ExtractorResponse
from app.schemas.validators import (
    LLMOutputValidationError,
    validate_extractor_output,
)
from app.services.llm import GeminiService, LLMProviderError, gemini_service

logger = logging.getLogger("blind_spot.extractor")


class ExtractorServiceError(Exception):
    """Raised when the Extractor service cannot produce a valid ExtractorResponse."""
    pass


class ExtractorService:
    """
    Coordinates the Extractor stage of the Blind Spot reasoning pipeline.
    Transforms raw user decision and reasoning into structured factors, assumptions, and conflicts.
    Enforces a strict 1-retry policy on malformed or invalid LLM output.
    """

    def __init__(self, llm: Optional[GeminiService] = None):
        self.llm = llm or gemini_service

    async def extract(self, decision: str, reasoning: str) -> ExtractorResponse:
        """
        Executes the extraction workflow with exactly one retry on schema/JSON validation failure.
        """
        user_prompt = build_extractor_user_prompt(decision, reasoning)

        # Attempt 1
        try:
            raw_output = await self.llm.generate_structured(
                system_prompt=EXTRACTOR_SYSTEM_PROMPT,
                user_prompt=user_prompt,
            )
            validated = validate_extractor_output(raw_output)
            logger.info("Extractor step completed successfully on initial attempt.")
            return validated
        except (LLMOutputValidationError, LLMProviderError, ValueError) as exc:
            logger.warning("Extractor attempt 1 validation failed (%s). Initiating retry attempt...", type(exc).__name__)

        # Attempt 2 (Retry once with reinforced schema instruction)
        retry_prompt = (
            f"IMPORTANT: The previous output failed schema validation. "
            f"Re-extract the reasoning and return ONLY a valid, single JSON object conforming strictly to the requested schema.\n\n"
            f"{user_prompt}"
        )

        try:
            raw_retry_output = await self.llm.generate_structured(
                system_prompt=EXTRACTOR_SYSTEM_PROMPT,
                user_prompt=retry_prompt,
            )
            validated_retry = validate_extractor_output(raw_retry_output)
            logger.info("Extractor step completed successfully on retry attempt.")
            return validated_retry
        except (LLMOutputValidationError, LLMProviderError, ValueError) as exc:
            logger.error("Extractor retry attempt failed (%s).", type(exc).__name__)
            raise ExtractorServiceError(
                "Unable to extract decision factors and assumptions from the provided input."
            ) from exc


# Default global instance for reuse
extractor_service = ExtractorService()
