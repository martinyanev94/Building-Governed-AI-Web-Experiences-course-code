from dataclasses import asdict, dataclass
import json
from typing import List


@dataclass
class AIProblemBrief:
    problem: str
    recent_views: List[str]
    capability: str
    output_shape: str
    success_criterion: str
    boundary: str


def build_brief() -> AIProblemBrief:
    return AIProblemBrief(
        problem="Help shoppers find relevant next products.",
        recent_views=["wireless keyboard", "desk lamp", "monitor stand"],
        capability="recommendation ranking",
        output_shape="ordered product IDs",
        success_criterion=(
            "Compare the rate at which shoppers select a recommended product "
            "with the rate for an equally visible random list."
        ),
        boundary=(
            "Recommendations assist discovery; they do not purchase products "
            "or remove ordinary search and browsing controls."
        ),
    )


def validate_brief(brief: AIProblemBrief) -> None:
    if not brief.problem:
        raise ValueError("problem must be concrete")
    if not brief.recent_views:
        raise ValueError("at least one input signal is required")
    if brief.capability != "recommendation ranking":
        raise ValueError("capability must match this lesson's example")
    if brief.output_shape != "ordered product IDs":
        raise ValueError("output must be an ordered list of product IDs")
    if not brief.success_criterion:
        raise ValueError("success criterion is required")
    if not brief.boundary:
        raise ValueError("user-control boundary is required")


if __name__ == "__main__":
    brief = build_brief()
    validate_brief(brief)
    print(json.dumps(asdict(brief), indent=2))
