from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Intent:
    goal: str
    topic: str
    level: str
    max_price: float


@dataclass(frozen=True)
class Candidate:
    title: str
    price: float
    level: str


def parse_intent(text: str) -> Intent:
    normalized = text.lower()
    price = re.search(r"under \$(\d+(?:\.\d+)?)", normalized)
    if not price or "python" not in normalized:
        raise ValueError("Expected a Python request with a price limit")
    level = "beginner" if "beginner" in normalized else "unspecified"
    return Intent("recommend", "Python", level, float(price.group(1)))


def rank_candidates(intent: Intent, candidates: list[Candidate]) -> list[Candidate]:
    eligible = [item for item in candidates if item.price <= intent.max_price]
    return sorted(
        eligible,
        key=lambda item: (item.level == intent.level, -item.price),
        reverse=True,
    )


def build_response(intent: Intent, ranked: list[Candidate]) -> dict:
    if not ranked:
        return {
            "status": "needs_clarification",
            "message": "No match found. Change the topic or price limit.",
            "controls": ["change_filters", "browse_all"],
        }
    top = ranked[0]
    return {
        "status": "ready",
        "recommendation": top.title,
        "reason": f"Matches {intent.topic}, {intent.level} level, under ${intent.max_price:.0f}.",
        "controls": ["useful", "not_useful", "change_filters"],
    }


def main() -> None:
    request = "I want a beginner Python book under $30"
    candidates = [
        Candidate("Python Basics", 24, "beginner"),
        Candidate("Practical Python", 29, "intermediate"),
        Candidate("Advanced Python", 35, "advanced"),
    ]
    intent = parse_intent(request)
    ranked = rank_candidates(intent, candidates)
    print(build_response(intent, ranked))


if __name__ == "__main__":
    main()
