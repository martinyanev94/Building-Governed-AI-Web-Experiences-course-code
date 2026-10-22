from src.final_review import PortfolioEvidence, assess_portfolio


def test_complete_evidence_allows_bounded_next_step():
    evidence = PortfolioEvidence(True, True, True, True)
    assert assess_portfolio(evidence) == "ready_for_next_step"


def test_missing_boundary_holds_review():
    evidence = PortfolioEvidence(True, True, True, False)
    assert assess_portfolio(evidence) == "hold_for_evidence"


def test_missing_measure_does_not_become_approval():
    evidence = PortfolioEvidence(True, True, False, True)
    assert assess_portfolio(evidence) == "hold_for_evidence"
