from src.architecture import (
    choose_adaptation,
    make_decision,
    record_event,
)


def test_decision_preserves_version_and_evidence():
    decision = make_decision("Moon", "ranker-v2", "science-fiction", "science-fiction")

    assert decision.model_version == "ranker-v2"
    assert decision.title == "Moon"
    assert decision.explanation == "matched requested genre science-fiction"
    assert "requested_genre=science-fiction" in decision.evidence


def test_monitoring_event_connects_decision_to_request():
    decision = make_decision("Moon", "ranker-v2", "science-fiction", "science-fiction")

    event = record_event(decision, "req-43", 240)

    assert event.request_id == "req-43"
    assert event.model_version == "ranker-v2"
    assert event.latency_ms == 240
    assert event.outcome == "Moon"
    assert event.explanation_source == "decision_evidence"


def test_adaptation_policy_is_explicit():
    assert choose_adaptation(84) == "keep_current_service"
    assert choose_adaptation(240) == "recommend_async_pipeline"


def test_fallback_explanation_does_not_claim_a_genre_match():
    decision = make_decision("Moon", "ranker-v2", "comedy", "science-fiction")

    assert decision.explanation == "selected by catalog fallback"
