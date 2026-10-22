from dataclasses import dataclass


@dataclass(frozen=True)
class TestRisk:
    name: str
    category: str
    impact: int
    likelihood: int
    evidence: str

    @property
    def priority(self) -> int:
        return self.impact * self.likelihood


RISKS = [
    TestRisk("protect history", "security", 5, 4, "cross-user history request is denied"),
    TestRisk("exclude watched titles", "validity", 5, 4, "watched title never appears in results"),
    TestRisk("compare director coverage", "bias", 4, 3, "coverage is compared across groups"),
    TestRisk("survive repeated requests", "reliability", 4, 3, "same valid request keeps its contract"),
    TestRisk("stay responsive under load", "performance", 3, 3, "response remains within the agreed target"),
]


def prioritize(risks: list[TestRisk]) -> list[TestRisk]:
    return sorted(risks, key=lambda risk: (-risk.priority, risk.name))


def matrix_rows(risks: list[TestRisk]) -> list[dict[str, object]]:
    return [
        {
            "priority": risk.priority,
            "category": risk.category,
            "test": risk.name,
            "evidence": risk.evidence,
        }
        for risk in prioritize(risks)
    ]


if __name__ == "__main__":
    for row in matrix_rows(RISKS):
        print(row)
