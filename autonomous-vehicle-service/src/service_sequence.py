from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"


@dataclass(frozen=True)
class ServiceRequest:
    vehicle_id: str
    transaction_id: str
    identity_verified: Optional[bool]
    permission_granted: Optional[bool]
    station_ready: Optional[bool]
    confirmed: Optional[bool]


@dataclass(frozen=True)
class PolicyDecision:
    decision: Decision
    reason: str


@dataclass(frozen=True)
class Dispute:
    transaction_id: str
    reason: str
    status: str = "dispute_open"


@dataclass(frozen=True)
class ImprovementProposal:
    trigger: str
    evidence_count: int
    status: str = "proposed"


ALLOWED_FEEDBACK = {"station_readiness_unknown", "amount_mismatch"}


def evaluate_policy(request: ServiceRequest) -> PolicyDecision:
    if request.identity_verified is not True:
        return PolicyDecision(Decision.REVIEW, "identity_not_verified")
    if request.permission_granted is False:
        return PolicyDecision(Decision.DENY, "permission_not_granted")
    if request.permission_granted is None:
        return PolicyDecision(Decision.REVIEW, "permission_unknown")
    if request.station_ready is not True:
        return PolicyDecision(Decision.REVIEW, "station_readiness_unknown")
    if request.confirmed is not True:
        return PolicyDecision(Decision.REVIEW, "explicit_confirmation_required")
    return PolicyDecision(Decision.ALLOW, "ready_for_service")


def open_dispute(transaction_id: str, reason: str) -> Dispute:
    if not transaction_id or not reason:
        raise ValueError("dispute_requires_transaction_and_reason")
    return Dispute(transaction_id=transaction_id, reason=reason)


def propose_improvement(event_reason: str, count: int) -> ImprovementProposal:
    if event_reason not in ALLOWED_FEEDBACK or count < 1:
        raise ValueError("feedback_not_actionable")
    return ImprovementProposal(trigger=event_reason, evidence_count=count)


if __name__ == "__main__":
    request = ServiceRequest("AV-204", "TX-204", True, True, None, True)
    print(evaluate_policy(request))
    print(open_dispute("TX-204", "amount_mismatch"))
    print(propose_improvement("station_readiness_unknown", 3))
