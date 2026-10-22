from src.compare_approaches import evaluate_galleryguide, pilot_decision


def test_galleryguide_is_ready_for_a_reviewed_pilot():
    decision = evaluate_galleryguide()
    assert pilot_decision(
        decision.user_value,
        decision.accessibility_tested,
        decision.safety_controls,
        decision.governance_owner,
        decision.fallback_ready,
    ) == "pilot_with_review"


def test_missing_fallback_holds_the_pilot():
    assert pilot_decision(True, True, True, "museum-platform-team", False) == "hold"


def test_blank_owner_holds_the_pilot():
    assert pilot_decision(True, True, True, "   ", True) == "hold"
