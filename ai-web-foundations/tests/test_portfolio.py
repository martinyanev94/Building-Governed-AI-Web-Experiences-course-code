from src.portfolio import Portfolio, assemble_portfolio


def complete_portfolio() -> Portfolio:
    return Portfolio(
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


def test_complete_portfolio_is_ready_for_review():
    assert assemble_portfolio(complete_portfolio()) == "ready_for_review"


def test_automatic_boundary_is_held():
    portfolio = complete_portfolio()
    automatic = Portfolio(
        artifacts=portfolio.artifacts,
        links=portfolio.links,
        automation_boundary="automatic",
        governance_rule=portfolio.governance_rule,
    )
    assert assemble_portfolio(automatic) == "hold: user-control boundary unresolved"


def test_missing_artifact_is_held():
    portfolio = complete_portfolio()
    incomplete = Portfolio(
        artifacts={key: value for key, value in portfolio.artifacts.items() if key != "tests"},
        links=portfolio.links,
        automation_boundary=portfolio.automation_boundary,
        governance_rule=portfolio.governance_rule,
    )
    assert assemble_portfolio(incomplete) == "hold: incomplete artifact set"
