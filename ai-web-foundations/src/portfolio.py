from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Portfolio:
    artifacts: Dict[str, str]
    links: List[Tuple[str, str]]
    automation_boundary: str
    governance_rule: str


def assemble_portfolio(portfolio: Portfolio) -> str:
    required = {"prototype", "architecture", "tests", "governance"}
    if set(portfolio.artifacts) != required:
        return "hold: incomplete artifact set"
    if any(
        source not in required or target not in required
        for source, target in portfolio.links
    ):
        return "hold: invalid traceability link"
    if portfolio.automation_boundary != "suggest_only":
        return "hold: user-control boundary unresolved"
    if portfolio.governance_rule != "confirmation_required":
        return "hold: governance control unresolved"
    return "ready_for_review"


if __name__ == "__main__":
    portfolio = Portfolio(
        artifacts={
            "prototype": "recommendation contract",
            "architecture": "five-boundary service map",
            "tests": "risk-based contract cases",
            "governance": "confirmation control",
        },
        links=[
            ("prototype", "architecture"),
            ("architecture", "tests"),
            ("tests", "governance"),
        ],
        automation_boundary="suggest_only",
        governance_rule="confirmation_required",
    )
    print(assemble_portfolio(portfolio))
