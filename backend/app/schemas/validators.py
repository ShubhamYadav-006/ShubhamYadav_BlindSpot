import json
from typing import Any, TypeVar, Type
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, ValidationError

from app.schemas.request import AnalyzeRequest
from app.schemas.response import (
    ExtractorResponse,
    ChallengerResponse,
    AnalyzeResponse,
)

T = TypeVar("T", bound=BaseModel)


class LLMOutputValidationError(ValueError):
    """Raised when LLM output cannot be parsed as JSON or violates schema constraints."""
    pass


def _parse_and_validate(model_cls: Type[T], raw_input: str | dict[str, Any]) -> T:
    """
    Parses a JSON string or dict and validates it strictly against the given Pydantic model.
    Does not silently repair invalid or malformed data.
    """
    if isinstance(raw_input, str):
        cleaned = raw_input.strip()
        # Handle optional markdown code fences ```json ... ``` if returned by LLMs
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise LLMOutputValidationError(f"Invalid JSON string: {exc}") from exc
    elif isinstance(raw_input, dict):
        parsed = raw_input
    else:
        raise LLMOutputValidationError(f"Expected str or dict, got {type(raw_input).__name__}")

    if not isinstance(parsed, dict):
        raise LLMOutputValidationError(f"Root JSON structure must be an object/dict, got {type(parsed).__name__}")

    try:
        return model_cls.model_validate(parsed)
    except ValidationError as exc:
        raise LLMOutputValidationError(f"Schema validation failed for {model_cls.__name__}: {exc}") from exc


def validate_extractor_output(data: str | dict[str, Any]) -> ExtractorResponse:
    """Validates raw output from the Extractor LLM step against ExtractorResponse schema."""
    return _parse_and_validate(ExtractorResponse, data)


def validate_challenger_output(data: str | dict[str, Any]) -> ChallengerResponse:
    """Validates raw output from the Challenger LLM step against ChallengerResponse schema."""
    return _parse_and_validate(ChallengerResponse, data)


def validate_final_response(data: str | dict[str, Any]) -> AnalyzeResponse:
    """Validates complete combined response against AnalyzeResponse schema."""
    return _parse_and_validate(AnalyzeResponse, data)


def validate_analyze_request(data: str | dict[str, Any]) -> AnalyzeRequest:
    """Validates request payload against AnalyzeRequest schema."""
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in request: {exc}") from exc
    elif isinstance(data, dict):
        parsed = data
    else:
        raise ValueError(f"Expected str or dict, got {type(data).__name__}")

    return AnalyzeRequest.model_validate(parsed)


def is_valid_extractor_output(data: str | dict[str, Any]) -> bool:
    """Returns True if the input conforms to ExtractorResponse, False otherwise."""
    try:
        validate_extractor_output(data)
        return True
    except (LLMOutputValidationError, ValueError):
        return False


def is_valid_challenger_output(data: str | dict[str, Any]) -> bool:
    """Returns True if the input conforms to ChallengerResponse, False otherwise."""
    try:
        validate_challenger_output(data)
        return True
    except (LLMOutputValidationError, ValueError):
        return False


def is_valid_final_response(data: str | dict[str, Any]) -> bool:
    """Returns True if the input conforms to AnalyzeResponse, False otherwise."""
    try:
        validate_final_response(data)
        return True
    except (LLMOutputValidationError, ValueError):
        return False


def merge_extractor_and_challenger(
    extractor: ExtractorResponse, challenger: ChallengerResponse
) -> AnalyzeResponse:
    """Combines validated Extractor and Challenger outputs into final AnalyzeResponse."""
    return AnalyzeResponse(
        decision=extractor.decision,
        stated_factors=extractor.stated_factors,
        assumptions=extractor.assumptions,
        conflicts=extractor.conflicts,
        blind_spots=challenger.blind_spots,
        questions=challenger.questions,
    )
