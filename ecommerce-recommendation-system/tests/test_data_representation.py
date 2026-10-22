from datetime import datetime

import pytest

from src.data_representation import EVENTS, make_inference_features, make_training_row


BACKPACK_ANCHOR = datetime.fromisoformat("2026-10-01T09:10:00")
WATER_ANCHOR = datetime.fromisoformat("2026-10-02T10:15:00")


def test_training_row_uses_completed_window_and_prior_features():
    row = make_training_row(EVENTS, "C17", "backpack-blue", BACKPACK_ANCHOR, True)
    assert row["view_count"] == 1
    assert row["cart_add_count"] == 1
    assert row["purchased_within_7_days"] == 1
    assert row["already_purchased"] is False


def test_inference_features_use_only_history_before_anchor():
    row = make_inference_features(EVENTS, "C17", "water-bottle", WATER_ANCHOR)
    assert row == {
        "customer_id": "C17",
        "item_id": "water-bottle",
        "view_count": 1,
        "cart_add_count": 1,
        "already_purchased": False,
    }
    assert "purchased_within_7_days" not in row


def test_incomplete_outcome_cannot_become_training_label():
    with pytest.raises(ValueError):
        make_training_row(EVENTS, "C17", "water-bottle", WATER_ANCHOR, False)


def test_future_purchase_does_not_change_live_features():
    later_events = EVENTS + [{
        "customer_id": "C17",
        "item_id": "water-bottle",
        "event_type": "purchase",
        "timestamp": datetime.fromisoformat("2026-10-04T12:00:00"),
    }]
    before = make_inference_features(EVENTS, "C17", "water-bottle", WATER_ANCHOR)
    after = make_inference_features(later_events, "C17", "water-bottle", WATER_ANCHOR)
    assert after == before
