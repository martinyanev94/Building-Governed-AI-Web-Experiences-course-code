from dataclasses import dataclass
import re


@dataclass(frozen=True)
class LanguageResult:
    intent: str
    entities: dict[str, object]
    response_action: str
    response_text: str


def preprocess(text: str) -> list[str]:
    """Normalize text into lowercase word-like tokens."""
    return re.findall(r"[a-z0-9']+", text.lower())


def interpret(text: str) -> tuple[str, dict[str, object]]:
    """Map a bounded set of language signals to an intent and entities."""
    tokens = preprocess(text)
    joined = " ".join(tokens)
    intent = "recommend_movie" if "movie" in tokens else "unknown"

    entities: dict[str, object] = {}
    if "funny" in tokens or "comedy" in tokens:
        entities["genre"] = "comedy"
    if "tonight" in tokens:
        entities["time"] = "tonight"
    entities["exclude_watched"] = "already watched" in joined
    return intent, entities


def select_response(
    text: str,
    watched_titles: set[str] | None = None,
) -> LanguageResult:
    """Apply response policy to the interpreted request and session context."""
    intent, entities = interpret(text)
    watched = watched_titles or set()

    if intent == "unknown":
        return LanguageResult(
            intent,
            entities,
            "clarify",
            "Tell me what kind of movie you want to watch.",
        )

    detail = entities.get("genre", "a movie")
    exclusion = " and exclude your watched titles" if watched else ""
    return LanguageResult(
        intent,
        entities,
        "recommend",
        f"I'll find {detail} movies{exclusion}.",
    )


if __name__ == "__main__":
    result = select_response(
        "I want a funny movie for tonight, not something I've already watched",
        watched_titles={"Dune"},
    )
    print(result)
