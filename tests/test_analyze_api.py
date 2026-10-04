from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.response import (
    AnalyzeResponse,
    BlindSpot,
    Conflict,
    ExtractorResponse,
    ChallengerResponse,
    Question,
    StatedFactor,
)
from app.services.challenger import ChallengerServiceError
from app.services.extractor import ExtractorServiceError

client = TestClient(app)

# Fixtures for mocked pipeline testing
MOCK_EXTRACTOR_OUTPUT = ExtractorResponse(
    decision="Take the six month internship",
    stated_factors=[
        StatedFactor(factor="good stipend", category="money"),
        StatedFactor(factor="nearby", category="convenience"),
    ],
    assumptions=[],
    conflicts=[],
)

MOCK_CHALLENGER_OUTPUT = ChallengerResponse(
    blind_spots=[
        BlindSpot(
            area="learning and career growth",
            why_it_matters_for_you="Your reasoning focuses mainly on money and convenience.",
        )
    ],
    questions=[
        Question(
            question="What would you want to learn during these six months?",
            linked_to="learning and career growth",
        )
    ],
)


# ==============================================================================
# TEST 1: Valid request -> 200 OK -> matches AnalyzeResponse schema
# ==============================================================================

@patch("app.routes.analyze.extractor_service.extract", new_callable=AsyncMock)
@patch("app.routes.analyze.challenger_service.challenge", new_callable=AsyncMock)
def test_valid_analyze_request(mock_challenge, mock_extract):
    mock_extract.return_value = MOCK_EXTRACTOR_OUTPUT
    mock_challenge.return_value = MOCK_CHALLENGER_OUTPUT

    payload = {
        "decision": "Should I accept the offer for a new role in Bangalore or stay at my current job?",
        "reasoning": "The new role pays 40% more and has faster promotions, but my current job has great stability.",
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    validated = AnalyzeResponse.model_validate(data)
    assert validated.decision == "Take the six month internship"
    assert len(validated.stated_factors) == 2
    assert len(validated.blind_spots) == 1
    assert len(validated.questions) == 1


# ==============================================================================
# TEST 2: Invalid request body -> 4xx (422) response
# ==============================================================================

def test_invalid_request_body():
    # Non-json or missing required fields
    response = client.post("/api/analyze", json={"unknown_key": "some value"})
    assert response.status_code == 422


# ==============================================================================
# TEST 3: Decision too short -> rejected (422)
# ==============================================================================

def test_decision_too_short():
    payload = {
        "decision": "Too short",
        "reasoning": "Valid reasoning string that contains more than twenty characters.",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TEST 4: Reasoning too short -> rejected (422)
# ==============================================================================

def test_reasoning_too_short():
    payload = {
        "decision": "Valid decision string that contains more than twenty characters.",
        "reasoning": "Too short",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TEST 5: Input exceeds maximum length -> rejected (422)
# ==============================================================================

def test_input_exceeds_maximum_length():
    oversized = "X" * 1501
    payload = {
        "decision": oversized,
        "reasoning": "Valid reasoning string that contains more than twenty characters.",
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422


# ==============================================================================
# TEST 6: Extractor failure -> controlled application error (503)
# ==============================================================================

@patch("app.routes.analyze.extractor_service.extract", new_callable=AsyncMock)
def test_extractor_failure_returns_controlled_error(mock_extract):
    mock_extract.side_effect = ExtractorServiceError("LLM failed after retry")

    payload = {
        "decision": "Valid decision text that meets the minimum length requirement.",
        "reasoning": "Valid reasoning text that meets the minimum length requirement.",
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 503
    assert "Unable to analyze decision reasoning" in response.json()["detail"]


# ==============================================================================
# TEST 7: Challenger failure -> controlled application error (503)
# ==============================================================================

@patch("app.routes.analyze.extractor_service.extract", new_callable=AsyncMock)
@patch("app.routes.analyze.challenger_service.challenge", new_callable=AsyncMock)
def test_challenger_failure_returns_controlled_error(mock_challenge, mock_extract):
    mock_extract.return_value = MOCK_EXTRACTOR_OUTPUT
    mock_challenge.side_effect = ChallengerServiceError("Guardrail failed after retry")

    payload = {
        "decision": "Valid decision text that meets the minimum length requirement.",
        "reasoning": "Valid reasoning text that meets the minimum length requirement.",
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 503
    assert "Unable to analyze decision reasoning" in response.json()["detail"]


# ==============================================================================
# TEST 8: Final response validation failure -> controlled application error
# ==============================================================================

@patch("app.routes.analyze.extractor_service.extract", new_callable=AsyncMock)
@patch("app.routes.analyze.challenger_service.challenge", new_callable=AsyncMock)
@patch("app.routes.analyze.validate_final_response")
def test_final_response_validation_failure(mock_validate, mock_challenge, mock_extract):
    mock_extract.return_value = MOCK_EXTRACTOR_OUTPUT
    mock_challenge.return_value = MOCK_CHALLENGER_OUTPUT
    mock_validate.side_effect = ValueError("Corrupted combined schema")

    payload = {
        "decision": "Valid decision text that meets the minimum length requirement.",
        "reasoning": "Valid reasoning text that meets the minimum length requirement.",
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 503


# ==============================================================================
# TEST 9: Extractor called before Challenger
# ==============================================================================

@patch("app.routes.analyze.extractor_service.extract", new_callable=AsyncMock)
@patch("app.routes.analyze.challenger_service.challenge", new_callable=AsyncMock)
def test_pipeline_execution_order(mock_challenge, mock_extract):
    call_order = []

    async def side_effect_extract(*args, **kwargs):
        call_order.append("extractor")
        return MOCK_EXTRACTOR_OUTPUT

    async def side_effect_challenge(*args, **kwargs):
        call_order.append("challenger")
        return MOCK_CHALLENGER_OUTPUT

    mock_extract.side_effect = side_effect_extract
    mock_challenge.side_effect = side_effect_challenge

    payload = {
        "decision": "Valid decision text that meets the minimum length requirement.",
        "reasoning": "Valid reasoning text that meets the minimum length requirement.",
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    assert call_order == ["extractor", "challenger"]


# ==============================================================================
# TEST 10: Challenger receives validated ExtractorResult
# ==============================================================================

@patch("app.routes.analyze.extractor_service.extract", new_callable=AsyncMock)
@patch("app.routes.analyze.challenger_service.challenge", new_callable=AsyncMock)
def test_challenger_receives_validated_extractor_result(mock_challenge, mock_extract):
    mock_extract.return_value = MOCK_EXTRACTOR_OUTPUT
    mock_challenge.return_value = MOCK_CHALLENGER_OUTPUT

    payload = {
        "decision": "Valid decision text that meets the minimum length requirement.",
        "reasoning": "Valid reasoning text that meets the minimum length requirement.",
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200

    # Verify mock_challenge was called with the exact output of mock_extract
    mock_challenge.assert_called_once_with(extractor_result=MOCK_EXTRACTOR_OUTPUT)


# ==============================================================================
# TEST 11: Verify endpoint does NOT call Gemini directly
# ==============================================================================

def test_route_does_not_contain_direct_gemini_client():
    """Verify route module only imports and calls high-level domain services."""
    import app.routes.analyze as route_module
    assert not hasattr(route_module, "genai")
    assert not hasattr(route_module, "GeminiService")


# ==============================================================================
# TEST 12: Verify no database dependency is introduced
# ==============================================================================

def test_no_database_dependency_in_api():
    """Verify application remains completely database-free."""
    import sys
    forbidden = ["sqlalchemy", "prisma", "psycopg", "motor", "pymongo"]
    for module in forbidden:
        assert module not in sys.modules


# ==============================================================================
# TEST 13: End-to-End Mocked Pipeline Test (from specification)
# ==============================================================================

@patch("app.routes.analyze.extractor_service.extract", new_callable=AsyncMock)
@patch("app.routes.analyze.challenger_service.challenge", new_callable=AsyncMock)
def test_end_to_end_mock_pipeline(mock_challenge, mock_extract):
    """
    Exact end-to-end test with inputs and outputs matching Prompt 5 Section 12.
    """
    input_payload = {
        "decision": "Take the six month internship because the stipend is good and it is nearby.",
        "reasoning": "I will save travel time and earn money, so I think it makes sense.",
    }

    mock_extract.return_value = ExtractorResponse(
        decision="Take the six month internship",
        stated_factors=[
            StatedFactor(factor="good stipend", category="money"),
            StatedFactor(factor="nearby", category="convenience"),
        ],
        assumptions=[],
        conflicts=[],
    )

    mock_challenge.return_value = ChallengerResponse(
        blind_spots=[
            BlindSpot(
                area="learning and career growth",
                why_it_matters_for_you="Your reasoning focuses mainly on money and convenience.",
            )
        ],
        questions=[
            Question(
                question="What would you want to learn during these six months?",
                linked_to="learning and career growth",
            )
        ],
    )

    response = client.post("/api/analyze", json=input_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["decision"] == "Take the six month internship"
    assert data["stated_factors"] == [
        {"factor": "good stipend", "category": "money"},
        {"factor": "nearby", "category": "convenience"},
    ]
    assert data["assumptions"] == []
    assert data["conflicts"] == []
    assert data["blind_spots"] == [
        {
            "area": "learning and career growth",
            "why_it_matters_for_you": "Your reasoning focuses mainly on money and convenience.",
        }
    ]
    assert data["questions"] == [
        {
            "question": "What would you want to learn during these six months?",
            "linked_to": "learning and career growth",
        }
    ]
