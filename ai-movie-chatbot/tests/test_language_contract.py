from src.language_contract import select_response


def test_movie_request_is_interpreted() -> None:
    result = select_response(
        "I want a funny movie for tonight, not something I've already watched",
        watched_titles={"Dune"},
    )

    assert result.intent == "recommend_movie"
    assert result.entities == {
        "genre": "comedy",
        "time": "tonight",
        "exclude_watched": True,
    }
    assert result.response_action == "recommend"
    assert result.response_text == "I'll find comedy movies and exclude your watched titles."


def test_missing_intent_requests_clarification() -> None:
    result = select_response("Show me something")

    assert result.intent == "unknown"
    assert result.response_action == "clarify"
    assert result.response_text == "Tell me what kind of movie you want to watch."


def test_preprocessing_is_case_insensitive() -> None:
    result = select_response("Find a FUNNY MOVIE")

    assert result.intent == "recommend_movie"
    assert result.entities["genre"] == "comedy"
