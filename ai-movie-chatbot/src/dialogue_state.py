from dataclasses import dataclass
from typing import Optional


@dataclass
class DialogueState:
    intent: Optional[str] = None
    genre: Optional[str] = None
    pending_field: Optional[str] = None
    watched_titles: tuple[str, ...] = ()


@dataclass
class ParsedRequest:
    intent: Optional[str] = None
    genre: Optional[str] = None


def advance(state: DialogueState, turn: ParsedRequest) -> tuple[DialogueState, str]:
    next_state = DialogueState(
        intent=turn.intent or state.intent,
        genre=turn.genre or state.genre,
        pending_field=state.pending_field,
        watched_titles=state.watched_titles,
    )

    if next_state.pending_field == "genre" and next_state.genre:
        next_state.pending_field = None

    if next_state.intent == "recommend_movie" and not next_state.genre:
        next_state.pending_field = "genre"
        return next_state, "What genre would you like?"

    if next_state.intent == "recommend_movie" and next_state.genre:
        return next_state, f"I’ll find a {next_state.genre} movie recommendation."

    return next_state, (
        "I can recommend a movie. Tell me a genre, "
        "such as comedy or drama."
    )
