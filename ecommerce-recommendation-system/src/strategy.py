from dataclasses import dataclass
from typing import Literal

Strategy = Literal["content_based", "hybrid", "behavior_based"]


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    history: tuple[str, ...]
    preferred_category: str | None
    content_signal_available: bool
    expected_item: str


def choose_strategy(case: EvaluationCase) -> Strategy:
    if not case.history:
        return "content_based"
    return "hybrid" if case.content_signal_available else "behavior_based"


def recommend_content(
    preferred_category: str | None,
    catalog: tuple[dict[str, object], ...],
) -> str:
    eligible = [
        item for item in catalog
        if item["available"]
        and (
            preferred_category is None
            or item["category"] == preferred_category
        )
    ]
    return str(eligible[0]["name"] if eligible else "No item")


def recommend_for_case(
    case: EvaluationCase,
    catalog: tuple[dict[str, object], ...],
) -> tuple[Strategy, str]:
    strategy = choose_strategy(case)
    if strategy == "content_based":
        item = recommend_content(case.preferred_category, catalog)
    else:
        item = str(catalog[0]["name"])
    return strategy, item


def evaluate_case(
    case: EvaluationCase,
    catalog: tuple[dict[str, object], ...],
) -> dict[str, object]:
    strategy, recommendation = recommend_for_case(case, catalog)
    return {
        "case": case.name,
        "strategy": strategy,
        "recommendation": recommendation,
        "hit": recommendation == case.expected_item,
    }


def top_one_hit_rate(records: list[dict[str, object]]) -> float:
    if not records:
        return 0.0
    return sum(bool(record["hit"]) for record in records) / len(records)
