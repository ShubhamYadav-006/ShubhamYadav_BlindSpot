# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    """
    Request payload schema for POST /api/analyze.
    Enforces minimum and maximum character lengths and trims leading/trailing whitespace.
    """
    decision: str = Field(
        ...,
        description="The decision the user is considering (20-1500 characters)",
        min_length=20,
        max_length=1500,
    )
    reasoning: str = Field(
        ...,
        description="Why the user is leaning toward this option (20-1500 characters)",
        min_length=20,
        max_length=1500,
    )

    @field_validator("decision", "reasoning", mode="before")
    @classmethod
    def validate_text(cls, value: object) -> str:
        if not isinstance(value, str):
            raise ValueError("Field must be a string.")
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Field cannot be empty or whitespace only.")
        if len(trimmed) < 20:
            raise ValueError("Field must be at least 20 characters long after trimming.")
        if len(trimmed) > 1500:
            raise ValueError("Field must not exceed 1500 characters after trimming.")
        return trimmed

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "decision": "Should I accept the offer for a new role in Bangalore or stay at my current job?",
                "reasoning": "The new role pays 40% more and has faster promotions, but my current job has great team culture and remote flexibility.",
            }
        },
    }
