import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from interaction_flow import Candidate, build_response, parse_intent, rank_candidates


def test_request_is_mapped_to_intent_and_ranked():
    intent = parse_intent("I want a beginner Python book under $30")
    candidates = [
        Candidate("Python Basics", 24, "beginner"),
        Candidate("Practical Python", 29, "intermediate"),
        Candidate("Advanced Python", 35, "advanced"),
    ]

    response = build_response(intent, rank_candidates(intent, candidates))

    assert intent.topic == "Python"
    assert intent.level == "beginner"
    assert intent.max_price == 30
    assert response["recommendation"] == "Python Basics"
    assert "under $30" in response["reason"]
    assert "change_filters" in response["controls"]


def test_no_eligible_candidate_requests_clarification():
    intent = parse_intent("I want a beginner Python book under $20")
    response = build_response(intent, rank_candidates(intent, [Candidate("Python Basics", 24, "beginner")]))

    assert response["status"] == "needs_clarification"
    assert "change_filters" in response["controls"]
