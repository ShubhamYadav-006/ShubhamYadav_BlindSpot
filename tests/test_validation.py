import json
import pytest
from pydantic import ValidationError

from app.schemas.request import AnalyzeRequest
from app.schemas.response import (
    VALID_FACTOR_CATEGORIES,
    StatedFactor,
    Assumption,
    Conflict,
    BlindSpot,
    Question,
    ExtractorResponse,
    ChallengerResponse,
    AnalyzeResponse,
)
from app.schemas.validators import (
    LLMOutputValidationError,
    validate_extractor_output,
    validate_challenger_output,
    validate_final_response,
    validate_analyze_request,
    is_valid_extractor_output,
    is_valid_challenger_output,
    is_valid_final_response,
    merge_extractor_and_challenger,
)


# ==============================================================================
# 1. REQUEST SCHEMA TESTS (AnalyzeRequest)
# ==============================================================================

def test_valid_request():
    """A valid decision and reasoning should pass validation."""
    data = {
        "decision": "Should I take an internship at a high-growth AI startup?",
        "reasoning": "The startup offers strong mentorship and fast promotion opportunities, though pay is lower.",
    }
    req = AnalyzeRequest(**data)
    assert req.decision == data["decision"]
    assert req.reasoning == data["reasoning"]


def test_request_too_short():
    """Input shorter than 20 characters should fail."""
    with pytest.raises(ValidationError):
        AnalyzeRequest(
            decision="Too short",
            reasoning="The startup offers strong mentorship and fast promotion opportunities.",
        )

    with pytest.raises(ValidationError):
        AnalyzeRequest(
            decision="Should I take an internship at a high-growth AI startup?",
            reasoning="Too short",
        )


def test_request_too_long():
    """Input longer than 1500 characters should fail."""
    oversized_text = "A" * 1501
    with pytest.raises(ValidationError):
        AnalyzeRequest(
            decision=oversized_text,
            reasoning="Valid reasoning text that exceeds twenty characters in length.",
        )

    with pytest.raises(ValidationError):
        AnalyzeRequest(
            decision="Valid decision text that exceeds twenty characters in length.",
            reasoning=oversized_text,
        )


def test_request_empty():
    """Empty strings should fail."""
    with pytest.raises(ValidationError):
        AnalyzeRequest(decision="", reasoning="Valid reasoning text that exceeds twenty characters in length.")

    with pytest.raises(ValidationError):
        AnalyzeRequest(decision="Valid decision text that exceeds twenty characters in length.", reasoning="")


def test_request_whitespace_only():
    """Whitespace-only input should fail."""
    with pytest.raises(ValidationError):
        AnalyzeRequest(
            decision="                        ",
            reasoning="Valid reasoning text that exceeds twenty characters in length.",
        )


def test_request_whitespace_trimming():
    """Leading and trailing whitespace should be trimmed, then length validated."""
    req = AnalyzeRequest(
        decision="   Should I move to Bangalore for the new job offer?   ",
        reasoning="   The company offers great growth and learning opportunities for engineers.   ",
    )
    assert req.decision == "Should I move to Bangalore for the new job offer?"
    assert req.reasoning == "The company offers great growth and learning opportunities for engineers."


def test_request_missing_fields():
    """Missing required fields in request should fail."""
    with pytest.raises(ValidationError):
        AnalyzeRequest(decision="Valid decision text that exceeds twenty characters in length.")  # type: ignore

    with pytest.raises(ValidationError):
        AnalyzeRequest(reasoning="Valid reasoning text that exceeds twenty characters in length.")  # type: ignore


def test_request_extra_fields_forbidden():
    """Extra unexpected fields should be rejected."""
    with pytest.raises(ValidationError):
        AnalyzeRequest(
            decision="Valid decision text that exceeds twenty characters in length.",
            reasoning="Valid reasoning text that exceeds twenty characters in length.",
            extra_field="malicious or unexpected data",  # type: ignore
        )


# ==============================================================================
# 2. STATED FACTOR SCHEMA TESTS
# ==============================================================================

@pytest.mark.parametrize("category", VALID_FACTOR_CATEGORIES)
def test_stated_factor_valid_categories(category):
    """All 8 allowed categories must pass validation."""
    factor = StatedFactor(factor="Higher compensation", category=category)
    assert factor.factor == "Higher compensation"
    assert factor.category == category


def test_stated_factor_invalid_category():
    """Categories outside the locked 8 must fail."""
    with pytest.raises(ValidationError):
        StatedFactor(factor="salary", category="invalid_category")  # type: ignore

    with pytest.raises(ValidationError):
        StatedFactor(factor="salary", category="finance")  # type: ignore


def test_stated_factor_empty_string():
    """Empty or whitespace-only factor text must fail."""
    with pytest.raises(ValidationError):
        StatedFactor(factor="", category="money")

    with pytest.raises(ValidationError):
        StatedFactor(factor="   ", category="money")


# ==============================================================================
# 3. ASSUMPTION & CONFLICT SCHEMA TESTS
# ==============================================================================

def test_assumption_valid():
    """Valid assumption must pass."""
    item = Assumption(
        assumption="Startups always lead to faster learning",
        why_risky="Poor management could mean lack of mentorship",
    )
    assert item.assumption == "Startups always lead to faster learning"
    assert item.why_risky == "Poor management could mean lack of mentorship"


def test_assumption_empty_fields():
    """Empty fields in assumption must fail."""
    with pytest.raises(ValidationError):
        Assumption(assumption="", why_risky="Some risk")

    with pytest.raises(ValidationError):
        Assumption(assumption="Some assumption", why_risky="  ")


def test_conflict_valid():
    """Valid conflict must pass."""
    item = Conflict(
        conflict="Desire for high income vs wanting low-stress work",
        explanation="High-paying consulting roles typically require 60+ hour workweeks",
    )
    assert item.conflict == "Desire for high income vs wanting low-stress work"
    assert item.explanation == "High-paying consulting roles typically require 60+ hour workweeks"


def test_conflict_empty_fields():
    """Empty fields in conflict must fail."""
    with pytest.raises(ValidationError):
        Conflict(conflict="", explanation="Explanation")

    with pytest.raises(ValidationError):
        Conflict(conflict="Conflict", explanation="")


# ==============================================================================
# 4. BLIND SPOT & QUESTION SCHEMA TESTS
# ==============================================================================

def test_blind_spot_valid():
    """Valid blind spot must pass."""
    spot = BlindSpot(
        area="Cost of Living and Relocation Expenses",
        why_it_matters_for_you="A 20% salary increase might be offset by 50% higher rent in Mumbai",
    )
    assert spot.area == "Cost of Living and Relocation Expenses"
    assert spot.why_it_matters_for_you == "A 20% salary increase might be offset by 50% higher rent in Mumbai"


def test_blind_spot_empty_fields():
    """Empty fields in blind spot must fail."""
    with pytest.raises(ValidationError):
        BlindSpot(area="", why_it_matters_for_you="Context")

    with pytest.raises(ValidationError):
        BlindSpot(area="Area", why_it_matters_for_you="   ")


def test_question_valid():
    """Valid Socratic question must pass."""
    q = Question(
        question="What specific mentorship evidence did you see during the interviews?",
        linked_to="Assumption about learning speed",
    )
    assert q.question == "What specific mentorship evidence did you see during the interviews?"
    assert q.linked_to == "Assumption about learning speed"


def test_question_empty_fields():
    """Empty fields in question must fail."""
    with pytest.raises(ValidationError):
        Question(question="", linked_to="Assumption")

    with pytest.raises(ValidationError):
        Question(question="Question?", linked_to="")


# ==============================================================================
# 5. EXTRACTOR RESPONSE & VALIDATOR TESTS
# ==============================================================================

def test_valid_extractor_response():
    """A valid ExtractorResponse model and validation helper must succeed."""
    data = {
        "decision": "Accept offer at Startup X",
        "stated_factors": [
            {"factor": "Higher potential equity", "category": "money"},
            {"factor": "Leadership responsibility", "category": "career"},
        ],
        "assumptions": [
            {"assumption": "The equity will be liquid within 3 years", "why_risky": "Startups frequently fail or stay private"}
        ],
        "conflicts": [
            {"conflict": "Wanting work-life balance vs joining early-stage startup", "explanation": "Early stage demands heavy overtime"}
        ],
    }
    res = validate_extractor_output(data)
    assert res.decision == "Accept offer at Startup X"
    assert len(res.stated_factors) == 2
    assert len(res.assumptions) == 1
    assert len(res.conflicts) == 1
    assert is_valid_extractor_output(data) is True


def test_invalid_extractor_json_malformed():
    """Malformed JSON string for Extractor must raise LLMOutputValidationError."""
    invalid_json_str = '{"decision": "Accept offer", "stated_factors": [broken json'
    with pytest.raises(LLMOutputValidationError):
        validate_extractor_output(invalid_json_str)
    assert is_valid_extractor_output(invalid_json_str) is False


def test_invalid_extractor_wrong_category():
    """Extractor output with invalid factor category must fail."""
    data = {
        "decision": "Accept offer",
        "stated_factors": [
            {"factor": "High pay", "category": "invalid_category"}
        ],
        "assumptions": [],
        "conflicts": [],
    }
    with pytest.raises(LLMOutputValidationError):
        validate_extractor_output(data)
    assert is_valid_extractor_output(data) is False


def test_invalid_extractor_missing_required():
    """Extractor output missing decision or other required keys must fail."""
    data = {
        "stated_factors": [],
        "assumptions": [],
        "conflicts": [],
    }
    with pytest.raises(LLMOutputValidationError):
        validate_extractor_output(data)


# ==============================================================================
# 6. CHALLENGER RESPONSE & VALIDATOR TESTS
# ==============================================================================

def test_valid_challenger_response():
    """A valid ChallengerResponse model and validation helper must succeed."""
    data = {
        "blind_spots": [
            {
                "area": "Runway and Cash Flow Risk",
                "why_it_matters_for_you": "Startup has only 9 months of runway left.",
            }
        ],
        "questions": [
            {
                "question": "How will you handle job security if funding rounds stall?",
                "linked_to": "Runway and Cash Flow Risk",
            },
            {
                "question": "What is your plan if the promotion timeline is delayed by a year?",
                "linked_to": "Career growth expectation",
            },
        ],
    }
    res = validate_challenger_output(data)
    assert len(res.blind_spots) == 1
    assert len(res.questions) == 2
    assert is_valid_challenger_output(data) is True


def test_invalid_challenger_json_malformed():
    """Malformed Challenger output must fail validation."""
    data = {
        "blind_spots": [
            {"area": "Missing why it matters"}  # missing why_it_matters_for_you
        ],
        "questions": [],
    }
    with pytest.raises(LLMOutputValidationError):
        validate_challenger_output(data)
    assert is_valid_challenger_output(data) is False


def test_challenger_json_with_markdown_fences():
    """JSON wrapped in markdown fences should be cleanly parsed and validated."""
    fenced_str = """```json
    {
      "blind_spots": [
        {
          "area": "Team Turnover",
          "why_it_matters_for_you": "Three seniors left in 6 months."
        }
      ],
      "questions": [
        {
          "question": "Have you spoken with former engineers from that team?",
          "linked_to": "Team Turnover"
        }
      ]
    }
    ```"""
    res = validate_challenger_output(fenced_str)
    assert len(res.blind_spots) == 1
    assert res.blind_spots[0].area == "Team Turnover"


# ==============================================================================
# 7. FINAL COMPLETE RESPONSE TESTS (AnalyzeResponse)
# ==============================================================================

def test_valid_complete_response():
    """A correctly structured complete AnalyzeResponse must pass."""
    data = {
        "decision": "Accept startup offer",
        "stated_factors": [
            {"factor": "Higher compensation", "category": "money"},
            {"factor": "Role scope", "category": "career"},
        ],
        "assumptions": [
            {"assumption": "Rapid career progression", "why_risky": "No structured review cycles"}
        ],
        "conflicts": [
            {"conflict": "Work hours vs health goals", "explanation": "Startup pace clashes with gym schedule"}
        ],
        "blind_spots": [
            {"area": "Market competition", "why_it_matters_for_you": "Two well-funded competitors launched recently"}
        ],
        "questions": [
            {"question": "How will you maintain health routines during product launch crunches?", "linked_to": "Work hours vs health goals"}
        ],
    }
    res = validate_final_response(data)
    assert res.decision == "Accept startup offer"
    assert len(res.stated_factors) == 2
    assert len(res.assumptions) == 1
    assert len(res.conflicts) == 1
    assert len(res.blind_spots) == 1
    assert len(res.questions) == 1
    assert is_valid_final_response(data) is True


def test_merge_extractor_and_challenger():
    """Merging valid Extractor and Challenger outputs must yield a valid AnalyzeResponse."""
    extractor = ExtractorResponse(
        decision="Relocate to Seattle",
        stated_factors=[StatedFactor(factor="Proximity to HQ", category="career")],
        assumptions=[Assumption(assumption="Rain won't affect mood", why_risky="Seasonal affective impact is real")],
        conflicts=[],
    )
    challenger = ChallengerResponse(
        blind_spots=[BlindSpot(area="Social Isolation", why_it_matters_for_you="No existing network in Seattle")],
        questions=[Question(question="How will you build a new support system?", linked_to="Social Isolation")],
    )
    merged = merge_extractor_and_challenger(extractor, challenger)
    assert merged.decision == "Relocate to Seattle"
    assert len(merged.stated_factors) == 1
    assert len(merged.assumptions) == 1
    assert len(merged.conflicts) == 0
    assert len(merged.blind_spots) == 1
    assert len(merged.questions) == 1


def test_request_validation_helper():
    """validate_analyze_request helper function should validate JSON string and dict."""
    valid_dict = {
        "decision": "Should I pursue a Master's degree in Computer Science?",
        "reasoning": "I want to specialize in distributed systems and research, but tuition is expensive.",
    }
    req = validate_analyze_request(valid_dict)
    assert req.decision == valid_dict["decision"]

    req_from_json = validate_analyze_request(json.dumps(valid_dict))
    assert req_from_json.reasoning == valid_dict["reasoning"]

    with pytest.raises(ValueError):
        validate_analyze_request("invalid json")
