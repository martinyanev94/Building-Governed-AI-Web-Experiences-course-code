from collections import defaultdict
from typing import Iterable


def evaluate(records: Iterable[dict]) -> dict:
    rows = list(records)
    total = len(rows)
    usefulness = (
        sum(row["task_completed"] for row in rows) / total
        if total else 0.0
    )

    by_mode = defaultdict(lambda: {"completed": 0, "total": 0})
    for row in rows:
        mode = row["input_mode"]
        by_mode[mode]["total"] += 1
        by_mode[mode]["completed"] += int(row["task_completed"])

    accessibility = {
        mode: values["completed"] / values["total"]
        for mode, values in by_mode.items()
    }
    harm_rate = sum(row["harmful"] for row in rows) / total if total else 0.0
    correction_rate = sum(row["corrected"] for row in rows) / total if total else 0.0

    return {
        "usefulness": usefulness,
        "accessibility_by_mode": dict(accessibility),
        "harm_rate": harm_rate,
        "correction_rate": correction_rate,
    }


SAMPLE_RECORDS = [
    {
        "user_id": "u1",
        "input_mode": "keyboard",
        "task_completed": True,
        "corrected": False,
        "harmful": False,
        "keyboard_navigation_failed": False,
        "screen_reader_action_unavailable": False,
    },
    {
        "user_id": "u2",
        "input_mode": "voice",
        "task_completed": True,
        "corrected": True,
        "harmful": False,
        "correction_reason": "preference_mismatch",
        "review_status": "reviewed",
    },
    {
        "user_id": "u3",
        "input_mode": "keyboard",
        "task_completed": False,
        "corrected": True,
        "harmful": True,
        "correction_reason": "unsuitable_recommendation",
        "review_status": "reviewed",
        "harm_reason": "unsuitable_recommendation",
    },
    {
        "user_id": "u4",
        "input_mode": "screen_reader",
        "task_completed": True,
        "corrected": False,
        "harmful": False,
        "screen_reader_action_unavailable": False,
    },
]


if __name__ == "__main__":
    print(evaluate(SAMPLE_RECORDS))
