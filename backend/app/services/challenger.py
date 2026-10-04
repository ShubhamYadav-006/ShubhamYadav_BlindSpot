import logging
from typing import Optional

from app.prompts.challenger import (
    CHALLENGER_SYSTEM_PROMPT,
    build_challenger_user_prompt,
)
from app.schemas.response import ChallengerResponse, ExtractorResponse
from app.schemas.validators import (
    LLMOutputValidationError,
    validate_challenger_output,
)
from app.services.guardrails import (
    RecommendationDetectedError,
    validate_challenger_guardrails,
)
from app.services.llm import GeminiService, LLMProviderError, gemini_service

logger = logging.getLogger("blind_spot.challenger")


class ChallengerServiceError(Exception):
    """Raised when the Challenger service cannot produce a valid, non-prescriptive ChallengerResponse."""
    pass


class ChallengerService:
    """
    Coordinates the Challenger stage of the Blind Spot reasoning pipeline.
    Transforms extracted reasoning into blind spots and Socratic reflection questions.
    Enforces a strict 1-retry policy on malformed output or recommendation language detection.
    """

    def __init__(self, llm: Optional[GeminiService] = None):
        self.llm = llm or gemini_service

    async def challenge(self, extractor_result: ExtractorResponse) -> ChallengerResponse:
        """
        Executes the challenger workflow with exactly one retry on schema failure or guardrail trigger.
        """
        user_prompt = build_challenger_user_prompt(extractor_result)

        # Attempt 1
        try:
            raw_output = await self.llm.generate_structured(
                system_prompt=CHALLENGER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
            )
            validated = validate_challenger_output(raw_output)
            validate_challenger_guardrails(validated)
            logger.info("Challenger step completed successfully on initial attempt.")
            return validated
        except (
            LLMOutputValidationError,
            RecommendationDetectedError,
            LLMProviderError,
            ValueError,
        ) as exc:
            logger.warning(
                "Challenger attempt 1 rejected (%s: %s). Initiating retry attempt...",
                type(exc).__name__,
                str(exc),
            )

        # Attempt 2 (Retry once with explicit non-prescriptive & schema reinforcement)
        retry_prompt = (
            f"IMPORTANT: The previous output failed validation or contained prescriptive recommendation language.\n"
            f"RULES REMINDER:\n"
            f"1. NEVER make a decision, recommend an option, or say 'you should'.\n"
            f"2. Output ONLY a valid JSON object matching the exact schema without markdown fences.\n\n"
            f"{user_prompt}"
        )

        try:
            raw_retry_output = await self.llm.generate_structured(
                system_prompt=CHALLENGER_SYSTEM_PROMPT,
                user_prompt=retry_prompt,
            )
            validated_retry = validate_challenger_output(raw_retry_output)
            validate_challenger_guardrails(validated_retry)
            logger.info("Challenger step completed successfully on retry attempt.")
            return validated_retry
        except (
            LLMOutputValidationError,
            RecommendationDetectedError,
            LLMProviderError,
            ValueError,
        ) as exc:
            logger.error("Challenger retry attempt failed (%s: %s).", type(exc).__name__, str(exc))
            raise ChallengerServiceError(
                "Unable to generate reflection questions and blind spots from the reasoning."
            ) from exc


# Default global instance for reuse
challenger_service = ChallengerService()
