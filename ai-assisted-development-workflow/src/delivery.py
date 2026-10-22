from dataclasses import dataclass


@dataclass(frozen=True)
class TestEvidence:
    risk_check_passed: bool


@dataclass(frozen=True)
class ReviewRecord:
    reviewer: str
    scope_approved: bool


@dataclass(frozen=True)
class ReleaseDecision:
    allowed: bool
    reason: str


def decide_release(
    tests: TestEvidence, review: ReviewRecord
) -> ReleaseDecision:
    if not tests.risk_check_passed:
        return ReleaseDecision(False, "risk check failed")
    if not review.scope_approved:
        return ReleaseDecision(False, "review scope not approved")
    return ReleaseDecision(True, "evidence complete")


def record_monitoring(version: str, outcome: str) -> dict[str, str]:
    return {"version": version, "outcome": outcome}


def rollback_target(version: str, outcome: str) -> str | None:
    if outcome == "rollback_required" and version == "v2":
        return "v1"
    return None
