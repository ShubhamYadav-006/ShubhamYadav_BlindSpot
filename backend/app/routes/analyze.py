import logging
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.schemas.validators import (
    LLMOutputValidationError,
    merge_extractor_and_challenger,
    validate_final_response,
)
from app.services.challenger import (
    ChallengerServiceError,
    challenger_service,
)
from app.services.extractor import (
    ExtractorServiceError,
    extractor_service,
)
from app.services.guardrails import RecommendationDetectedError
from app.services.llm import LLMProviderError
from app.services.rate_limit import rate_limit_dependency

logger = logging.getLogger("blind_spot.api")

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limit_dependency)],
    summary="Analyze decision reasoning and surface blind spots",
    description=(
        "Executes the stateless 2-stage AI analysis pipeline: "
        "Extractor stage extracts factors, assumptions, and conflicts; "
        "Challenger stage surfaces unconsidered blind spots and Socratic reflection questions. "
        "Rate-limited to approximately 5 requests per IP per minute."
    ),
)
async def analyze_decision(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Orchestrates the decision reflection workflow:
    1. Validates input request via AnalyzeRequest Pydantic model.
    2. Runs Extractor service to identify factors, assumptions, and conflicts.
    3. Runs Challenger service to generate blind spots and Socratic reflection questions.
    4. Merges and validates the combined FinalResponse before returning.
    """
    try:
        # Step 1: Extractor Stage
        extractor_result = await extractor_service.extract(
            decision=request.decision,
            reasoning=request.reasoning,
        )

        # Step 2: Challenger Stage
        challenger_result = await challenger_service.challenge(
            extractor_result=extractor_result
        )

        # Step 3: Combine into Final Response
        combined_response = merge_extractor_and_challenger(
            extractor=extractor_result,
            challenger=challenger_result,
        )

        # Step 4: Final output validation
        validated_response = validate_final_response(combined_response.model_dump())
        return validated_response

    except (
        ExtractorServiceError,
        ChallengerServiceError,
        LLMProviderError,
        LLMOutputValidationError,
        RecommendationDetectedError,
        ValueError,
    ) as exc:
        logger.error("Analysis pipeline failed (%s: %s)", type(exc).__name__, str(exc))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to analyze decision reasoning at this time. Please try again.",
        ) from None
    except Exception as exc:
        logger.error("Unexpected error in /api/analyze: %s", type(exc).__name__)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request.",
        ) from None
