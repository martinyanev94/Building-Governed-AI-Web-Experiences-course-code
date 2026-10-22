from strategy import EvaluationCase, evaluate_case, top_one_hit_rate


CATALOG = (
    {"name": "Trail Bottle", "category": "outdoor", "available": True},
    {"name": "Desk Lamp", "category": "home", "available": True},
    {"name": "Rain Jacket", "category": "outdoor", "available": False},
)


if __name__ == "__main__":
    new_shopper = EvaluationCase(
        name="new_shopper",
        history=(),
        preferred_category="outdoor",
        content_signal_available=True,
        expected_item="Trail Bottle",
    )
    record = evaluate_case(new_shopper, CATALOG)
    print(record)
    print(top_one_hit_rate([record]))
