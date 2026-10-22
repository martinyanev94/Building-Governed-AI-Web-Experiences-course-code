from src.main import handle_recommendation


def test_recommendation_uses_dialogue_state_and_excludes_watched_title():
    state = {
        "intent": "recommend_movie",
        "genre": "comedy",
        "exclude_watched": ["The Mask"],
    }
    assert handle_recommendation(state) == (
        "Try Game Night. It matches comedy and it isn't in your watched list."
    )


def test_missing_genre_requests_clarification():
    assert handle_recommendation({"intent": "recommend_movie"}) == (
        "What genre are you in the mood for?"
    )


def test_empty_eligible_catalog_uses_grounded_fallback():
    state = {
        "intent": "recommend_movie",
        "genre": "comedy",
        "exclude_watched": ["The Mask", "Game Night"],
    }
    assert handle_recommendation(state) == (
        "I couldn't find an unwatched comedy movie in the current catalog."
    )
