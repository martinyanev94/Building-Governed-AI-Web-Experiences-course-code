from dataclasses import dataclass, replace
from datetime import date
from typing import Literal


@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    layer: Literal["strategy", "governance", "management"]
    reference: str
    status: Literal["present", "gap"]
    evidence_ref: str = ""


@dataclass(frozen=True)
class ReviewRecord:
    system_id: str
    reviewed_on: date
    cadence_days: int
    objective: str
    evidence_checked: int
    open_gaps: tuple[str, ...]
    criteria_met: bool
    status: Literal["ready", "escalate"]


@dataclass(frozen=True)
class Escalation:
    gap_id: str
    reason: str
    owner: str
    next_review: date


def unresolved_requirements(requirements: list[Requirement]) -> list[Requirement]:
    return [
        item
        for item in requirements
        if item.status != "present" or not item.evidence_ref
    ]


def run_review(
    requirements: list[Requirement],
    system_id: str,
    reviewed_on: date,
    cadence_days: int = 30,
) -> ReviewRecord:
    objective = "Every requirement is present with evidence"
    checked = sum(bool(item.evidence_ref) for item in requirements)
    gaps = tuple(item.requirement_id for item in unresolved_requirements(requirements))
    criteria_met = not gaps
    return ReviewRecord(
        system_id=system_id,
        reviewed_on=reviewed_on,
        cadence_days=cadence_days,
        objective=objective,
        evidence_checked=checked,
        open_gaps=gaps,
        criteria_met=criteria_met,
        status="ready" if criteria_met else "escalate",
    )


def escalate(
    review: ReviewRecord,
    owner: str,
    next_review: date,
) -> tuple[Escalation, ...]:
    if review.status != "escalate":
        return ()
    if not owner.strip() or next_review is None:
        raise ValueError("escalation owner and next_review are required")
    return tuple(
        Escalation(gap, "missing evidence", owner, next_review)
        for gap in review.open_gaps
    )


if __name__ == "__main__":
    requirements = [
        Requirement("leadership-policy", "governance", "POL-01", "present", "policy-v3"),
        Requirement("model-inventory", "management", "INV-01", "present", "inventory-2026-10"),
        Requirement("performance-evaluation-review", "management", "PERF-01", "present"),
    ]
    review = run_review(requirements, "AV-204", date(2026, 10, 21))
    print(review)
    print(escalate(review, "governance-ops", date(2026, 11, 20)))
    updated_requirements = [
        *requirements[:2],
        replace(requirements[2], status="present", evidence_ref="evaluation-2026-10"),
    ]
    next_review = run_review(updated_requirements, "AV-204", date(2026, 11, 20))
    print(next_review)
