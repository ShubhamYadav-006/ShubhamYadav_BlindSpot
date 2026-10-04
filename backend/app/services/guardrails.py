import re
from typing import Optional, Tuple

from app.schemas.response import ChallengerResponse


class RecommendationDetectedError(ValueError):
    """Raised when recommendation or directive language is detected in LLM output."""
    pass


# Normalized patterns for recommendation and directive advice detection
RECOMMENDATION_PATTERNS = [
    r"\byou should\b",
    r"\byou must choose\b",
    r"\bi recommend\b",
    r"\bi suggest you choose\b",
    r"\bi suggest you\b",
    r"\bbest option\b",
    r"\bdefinitely choose\b",
    r"\bgo with\b",
    r"\byou ought to\b",
    r"\bthe better choice\b",
    r"\bbetter option\b",
    r"\bchoose (?:the|option|this|that|x)\b",
    r"\bpick (?:the|option|this|that|x)\b",
]

_COMPILED_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in RECOMMENDATION_PATTERNS
]


def scan_text_for_recommendations(text: str) -> Tuple[bool, Optional[str]]:
    """
    Normalizes whitespace and case, then scans text for recommendation phrases.
    Returns (True, matched_pattern) if a recommendation is found, else (False, None).
    """
    if not text:
        return False, None
    normalized = " ".join(text.lower().split())
    for pattern in _COMPILED_PATTERNS:
        match = pattern.search(normalized)
        if match:
            return True, match.group(0)
    return False, None


def validate_challenger_guardrails(challenger: ChallengerResponse) -> None:
    """
    Validates that a ChallengerResponse contains no directive recommendations in any text field.
    Raises RecommendationDetectedError if prescriptive language is detected.
    """
    for index, spot in enumerate(challenger.blind_spots):
        has_rec, match = scan_text_for_recommendations(spot.area)
        if has_rec:
            raise RecommendationDetectedError(
                f"Blind spot #{index + 1} area contains recommendation phrase: '{match}'"
            )
        has_rec, match = scan_text_for_recommendations(spot.why_it_matters_for_you)
        if has_rec:
            raise RecommendationDetectedError(
                f"Blind spot #{index + 1} why_it_matters_for_you contains recommendation phrase: '{match}'"
            )

    for index, q in enumerate(challenger.questions):
        has_rec, match = scan_text_for_recommendations(q.question)
        if has_rec:
            raise RecommendationDetectedError(
                f"Question #{index + 1} contains recommendation phrase: '{match}'"
            )
        has_rec, match = scan_text_for_recommendations(q.linked_to)
        if has_rec:
            raise RecommendationDetectedError(
                f"Question #{index + 1} linked_to contains recommendation phrase: '{match}'"
            )
