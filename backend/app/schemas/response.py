from typing import Literal
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, field_validator

# Strictly locked categories for StatedFactor
VALID_FACTOR_CATEGORIES = (
    "money",
    "convenience",
    "growth",
    "academics",
    "health",
    "relationships",
    "career",
    "other",
)

FactorCategory = Literal[
    "money",
    "convenience",
    "growth",
    "academics",
    "health",
    "relationships",
    "career",
    "other",
]


class BaseStrictModel(BaseModel):
    """Base model that forbids extra fields and rejects malformed inputs."""
    model_config = {
        "extra": "forbid",
        "str_strip_whitespace": True,
    }


def _validate_non_empty_str(value: object, field_name: str = "Field") -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")
    trimmed = value.strip()
    if not trimmed:
        raise ValueError(f"{field_name} cannot be empty or whitespace only.")
    return trimmed


class StatedFactor(BaseStrictModel):
    """Explicitly stated factor considered by the user."""
    factor: str = Field(..., min_length=1, description="The factor identified")
    category: FactorCategory = Field(..., description="Classification of the factor")

    @field_validator("factor", mode="before")
    @classmethod
    def validate_factor(cls, value: object) -> str:
        return _validate_non_empty_str(value, "factor")


class Assumption(BaseStrictModel):
    """Hidden or unstated assumption underlying the user's reasoning."""
    assumption: str = Field(..., min_length=1, description="The identified assumption")
    why_risky: str = Field(..., min_length=1, description="Why this assumption introduces risk")

    @field_validator("assumption", "why_risky", mode="before")
    @classmethod
    def validate_fields(cls, value: object) -> str:
        return _validate_non_empty_str(value)


class Conflict(BaseStrictModel):
    """Internal conflict or tension between goals/priorities."""
    conflict: str = Field(..., min_length=1, description="The identified conflict")
    explanation: str = Field(..., min_length=1, description="Explanation of why these clash")

    @field_validator("conflict", "explanation", mode="before")
    @classmethod
    def validate_fields(cls, value: object) -> str:
        return _validate_non_empty_str(value)


class ExtractorResponse(BaseStrictModel):
    """Structured extraction output from the Extractor LLM step."""
    decision: str = Field(..., min_length=1, description="Normalized decision statement")
    stated_factors: list[StatedFactor] = Field(..., description="Explicit factors")
    assumptions: list[Assumption] = Field(..., description="Assumptions")
    conflicts: list[Conflict] = Field(..., description="Conflicts")

    @field_validator("decision", mode="before")
    @classmethod
    def validate_decision(cls, value: object) -> str:
        return _validate_non_empty_str(value, "decision")


class BlindSpot(BaseStrictModel):
    """Overlooked angle or perspective."""
    area: str = Field(..., min_length=1, description="Overlooked domain or angle")
    why_it_matters_for_you: str = Field(..., min_length=1, description="Why this matters for the user's situation")

    @field_validator("area", "why_it_matters_for_you", mode="before")
    @classmethod
    def validate_fields(cls, value: object) -> str:
        return _validate_non_empty_str(value)


class Question(BaseStrictModel):
    """Socratic reflection question."""
    question: str = Field(..., min_length=1, description="The Socratic reflection question")
    linked_to: str = Field(..., min_length=1, description="What assumption, conflict, or blind spot this probes")

    @field_validator("question", "linked_to", mode="before")
    @classmethod
    def validate_fields(cls, value: object) -> str:
        return _validate_non_empty_str(value)


class ChallengerResponse(BaseStrictModel):
    """Output from the Challenger LLM step."""
    blind_spots: list[BlindSpot] = Field(..., description="Identified blind spots")
    questions: list[Question] = Field(..., description="5-7 Socratic reflection questions")


class AnalyzeResponse(BaseStrictModel):
    """Complete aggregated response for POST /api/analyze."""
    decision: str = Field(..., min_length=1, description="Normalized decision statement")
    stated_factors: list[StatedFactor] = Field(..., description="Stated factors")
    assumptions: list[Assumption] = Field(..., description="Assumptions")
    conflicts: list[Conflict] = Field(..., description="Conflicts")
    blind_spots: list[BlindSpot] = Field(..., description="Blind spots")
    questions: list[Question] = Field(..., description="Socratic reflection questions")

    @field_validator("decision", mode="before")
    @classmethod
    def validate_decision(cls, value: object) -> str:
        return _validate_non_empty_str(value, "decision")
