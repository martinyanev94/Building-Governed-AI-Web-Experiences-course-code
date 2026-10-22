import pytest

from src.movie_recommender import build_response, build_rationale, record_correction


def test_response_uses_selected_reason() -> None:
    response = build_response(
        "science fiction",
        {"Arrival": "science fiction", "Dune": "science fiction"},
        {"Solaris": "science fiction", "Amelie": "comedy"},
        {"Arrival", "Dune"},
    )
    assert response["movie"] == "Solaris"
    assert response["rationale"] == (
        "Recommended Solaris because you selected science fiction "
        "and your history includes science fiction movies."
    )


def test_empty_history_does_not_claim_behavior() -> None:
    rationale = build_rationale(
        "science fiction", {}, "Solaris", "preference_match"
    )
    assert rationale == "Recommended Solaris because you selected science fiction."


def test_fallback_rationale_is_honest() -> None:
    rationale = build_rationale(
        "science fiction", {}, "Amelie", "catalog_fallback"
    )
    assert rationale == (
        "Recommended Amelie as a catalog fallback because "
        "no unwatched science fiction movie was available."
    )


def test_correction_preserves_context() -> None:
    event = record_correction(
        "Solaris",
        "not_relevant",
        "science fiction",
        {"Arrival": "science fiction", "Dune": "science fiction"},
        {"Arrival", "Dune"},
        "preference_match",
    )
    assert event == {
        "movie": "Solaris",
        "correction": "not_relevant",
        "preference_at_request": "science fiction",
        "history": {
            "Arrival": "science fiction",
            "Dune": "science fiction",
        },
        "watched": ["Arrival", "Dune"],
        "selection_reason": "preference_match",
    }


def test_unknown_correction_is_rejected() -> None:
    with pytest.raises(ValueError):
        record_correction(
            "Solaris",
            "delete_preference",
            "science fiction",
            {},
            set(),
            "preference_match",
        )
