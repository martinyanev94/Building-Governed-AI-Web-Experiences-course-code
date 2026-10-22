from collections import Counter
from dataclasses import dataclass
from typing import Iterable

ALLOWED_FEEDBACK = {"wrong_product", "missing_product", "resolved"}


@dataclass(frozen=True)
class Feedback:
    category: str
    deployment_version: str


@dataclass(frozen=True)
class ImprovementProposal:
    proposed_version: str
    trigger: str


@dataclass(frozen=True)
class Evaluation:
    candidate_score: float
    baseline_score: float
    regression_found: bool


@dataclass(frozen=True)
class ReleaseRecord:
    version: str
    decision: str
    reason: str


def propose_improvement(
    feedback: Iterable[Feedback], current_version: str
) -> ImprovementProposal | None:
    counts = Counter(
        item.category for item in feedback if item.category in ALLOWED_FEEDBACK
    )
    if counts["wrong_product"] < 2:
        return None

    major, minor = map(int, current_version.split("."))
    return ImprovementProposal(
        proposed_version=f"{major}.{minor + 1}",
        trigger="review recommendation matching",
    )


def evaluate_candidate(
    candidate_score: float, baseline_score: float, regression_found: bool
) -> Evaluation:
    return Evaluation(candidate_score, baseline_score, regression_found)


def approve_release(
    proposal: ImprovementProposal | None, evaluation: Evaluation
) -> bool:
    return (
        proposal is not None
        and evaluation.candidate_score >= evaluation.baseline_score
        and not evaluation.regression_found
    )


def activate(
    current_version: str,
    proposal: ImprovementProposal | None,
    approved: bool,
) -> tuple[str, ReleaseRecord]:
    if proposal is None or not approved:
        return current_version, ReleaseRecord(
            current_version,
            "held",
            "evidence incomplete or regression found",
        )

    return proposal.proposed_version, ReleaseRecord(
        proposal.proposed_version,
        "activated",
        proposal.trigger,
    )
