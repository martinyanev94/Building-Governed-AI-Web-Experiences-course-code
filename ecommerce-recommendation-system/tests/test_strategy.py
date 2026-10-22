from src.strategy import (
    EvaluationCase,
    evaluate_case,
    recommend_content,
    choose_strategy,
    top_one_hit_rate,
)


CATALOG = (
    {"name": "Trail Bottle", "category": "outdoor", "available": True},
    {"name": "Desk Lamp", "category": "home", "available": True},
    {"name": "Rain Jacket", "category": "outdoor", "available": False},
)


def test_cold_start_filters_category_and_availability():
    assert recommend_content("outdoor", CATALOG) == "Trail Bottle"


def test_empty_category_uses_first_available_fallback():
    assert recommend_content(None, CATALOG) == "Trail Bottle"


def test_hybrid_requires_content_signal():
    case = EvaluationCase("history_only", ("Desk Lamp",), None, False, "Desk Lamp")
    assert choose_strategy(case) == "behavior_based"


def test_evaluation_connects_recommendation_to_hit():
    case = EvaluationCase("new_shopper", (), "outdoor", True, "Trail Bottle")
    assert evaluate_case(case, CATALOG)["hit"] is True


def test_top_one_hit_rate_aggregates_records():
    records = [{"hit": True}, {"hit": False}]
    assert top_one_hit_rate(records) == 0.5
