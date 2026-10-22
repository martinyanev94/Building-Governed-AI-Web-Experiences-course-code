from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ReviewRecord:
    intent: str
    files_changed: tuple[str, ...]
    tests_passed: bool
    risk_flags: tuple[str, ...]
    decision: str


def review_status(status: str) -> str:
    """Approve only the explicit approved status; fail closed otherwise."""
    if status == "approved":
        return "approved"
    return "needs_changes"


def create_review_record(
    intent: str,
    files_changed: Sequence[str],
    tests_passed: bool,
    risk_flags: Sequence[str],
) -> ReviewRecord:
    """Create a reviewable decision from scope, verification, and risk evidence."""
    files = tuple(files_changed)
    risks = tuple(risk_flags)
    decision = "approved"

    if not tests_passed or risks or not files:
        decision = "needs_changes"

    return ReviewRecord(
        intent=intent,
        files_changed=files,
        tests_passed=tests_passed,
        risk_flags=risks,
        decision=decision,
    )
