from datetime import datetime, timedelta
from typing import Any

Event = dict[str, Any]

EVENTS: list[Event] = [
    {"customer_id": "C17", "item_id": "backpack-blue", "event_type": "view", "timestamp": datetime.fromisoformat("2026-10-01T09:00:00")},
    {"customer_id": "C17", "item_id": "backpack-blue", "event_type": "add_to_cart", "timestamp": datetime.fromisoformat("2026-10-01T09:05:00")},
    {"customer_id": "C17", "item_id": "backpack-blue", "event_type": "purchase", "timestamp": datetime.fromisoformat("2026-10-01T18:00:00")},
    {"customer_id": "C17", "item_id": "water-bottle", "event_type": "view", "timestamp": datetime.fromisoformat("2026-10-02T10:00:00")},
    {"customer_id": "C17", "item_id": "water-bottle", "event_type": "add_to_cart", "timestamp": datetime.fromisoformat("2026-10-02T10:10:00")},
]


def history_for_item(events: list[Event], customer_id: str, item_id: str, prediction_at: datetime) -> list[Event]:
    return [
        event for event in events
        if event["customer_id"] == customer_id
        and event["item_id"] == item_id
        and event["timestamp"] < prediction_at
    ]


def count_behavior(history: list[Event]) -> dict[str, int]:
    counts = {"view": 0, "add_to_cart": 0}
    for event in history:
        if event["event_type"] in counts:
            counts[event["event_type"]] += 1
    return counts


def make_training_row(events: list[Event], customer_id: str, item_id: str, prediction_at: datetime, outcome_complete: bool) -> dict[str, Any]:
    if not outcome_complete:
        raise ValueError("Outcome window is not complete")
    history = history_for_item(events, customer_id, item_id, prediction_at)
    counts = count_behavior(history)
    window_end = prediction_at + timedelta(days=7)
    purchased = any(
        event["event_type"] == "purchase"
        and prediction_at <= event["timestamp"] <= window_end
        for event in events
        if event["customer_id"] == customer_id
        and event["item_id"] == item_id
    )
    return {
        "customer_id": customer_id,
        "item_id": item_id,
        "view_count": counts["view"],
        "cart_add_count": counts["add_to_cart"],
        "purchased_within_7_days": int(purchased),
        "already_purchased": any(event["event_type"] == "purchase" for event in history),
    }


def make_inference_features(events: list[Event], customer_id: str, item_id: str, prediction_at: datetime) -> dict[str, Any]:
    history = history_for_item(events, customer_id, item_id, prediction_at)
    counts = count_behavior(history)
    return {
        "customer_id": customer_id,
        "item_id": item_id,
        "view_count": counts["view"],
        "cart_add_count": counts["add_to_cart"],
        "already_purchased": any(event["event_type"] == "purchase" for event in history),
    }


if __name__ == "__main__":
    backpack_anchor = datetime.fromisoformat("2026-10-01T09:10:00")
    water_anchor = datetime.fromisoformat("2026-10-02T10:15:00")
    print(make_training_row(EVENTS, "C17", "backpack-blue", backpack_anchor, True))
    print(make_inference_features(EVENTS, "C17", "water-bottle", water_anchor))
