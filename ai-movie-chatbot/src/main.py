from .recommendation_service import recommend_from_state
from .response_templates import format_recommendation


def handle_recommendation(dialogue_state):
    if dialogue_state.get("intent") != "recommend_movie":
        return "Tell me what kind of movie you want."
    if not dialogue_state.get("genre"):
        return "What genre are you in the mood for?"

    results = recommend_from_state(dialogue_state)
    return format_recommendation(results, dialogue_state["genre"])


if __name__ == "__main__":
    state = {
        "intent": "recommend_movie",
        "genre": "comedy",
        "exclude_watched": ["The Mask"],
    }
    print(handle_recommendation(state))
