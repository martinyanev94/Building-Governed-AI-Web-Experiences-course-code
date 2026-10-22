from dataclasses import dataclass

@dataclass(frozen=True)
class Risk:
    risk_id: str
    mechanism: str
    user_impact: int
    business_impact: int
    likelihood: int
    owner: str

@dataclass(frozen=True)
class Control:
    risk_id: str
    name: str
    evidence: str

def prioritize_controls(risks: list[Risk], controls: list[Control]) -> list[dict]:
    control_by_risk = {item.risk_id: item for item in controls}
    decisions = []
    for risk in risks:
        control = control_by_risk[risk.risk_id]
        priority = risk.user_impact * risk.business_impact * risk.likelihood
        decisions.append({
            "risk_id": risk.risk_id,
            "mechanism": risk.mechanism,
            "owner": risk.owner,
            "priority": priority,
            "control": control.name,
            "evidence": control.evidence,
        })
    return sorted(decisions, key=lambda item: (-item["priority"], item["risk_id"]))

RISKS = [
    Risk("R-17", "Sensitive account context in explanation", 5, 4, 4, "Product risk owner"),
    Risk("R-18", "Stale recommendation after model drift", 3, 5, 3, "ModelOps owner"),
    Risk("R-19", "Tampered input changes recommendation", 4, 3, 2, "Application security owner"),
]

CONTROLS = [
    Control("R-17", "Privacy filter", "sampled explanations contain no protected fields"),
    Control("R-18", "Model monitoring", "versioned anomaly record and review decision"),
    Control("R-19", "Application security review", "input-integrity review"),
]
