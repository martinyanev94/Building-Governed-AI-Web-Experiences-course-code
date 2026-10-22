import pytest
from src.governance import CONTROLS, RISKS, prioritize_controls

def test_priority_order_owner_and_evidence():
    decisions = prioritize_controls(RISKS, CONTROLS)
    assert [item["risk_id"] for item in decisions] == ["R-17", "R-18", "R-19"]
    assert [item["priority"] for item in decisions] == [80, 45, 24]
    assert decisions[0]["owner"] == "Product risk owner"
    assert decisions[0]["evidence"] == "sampled explanations contain no protected fields"

def test_missing_control_fails_closed():
    with pytest.raises(KeyError):
        prioritize_controls([RISKS[0]], [])

def test_ties_are_deterministic():
    decisions = prioritize_controls([RISKS[0]], [CONTROLS[0]])
    assert decisions[0]["risk_id"] == "R-17"
