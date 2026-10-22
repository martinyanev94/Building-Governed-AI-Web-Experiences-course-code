from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioEvidence:
    has_user_problem: bool
    has_traceable_flow: bool
    has_success_measure: bool
    has_boundaries: bool


def assess_portfolio(evidence: PortfolioEvidence) -> str:
    """Return a fail-closed portfolio decision."""
    complete = all(vars(evidence).values())
    return "ready_for_next_step" if complete else "hold_for_evidence"
