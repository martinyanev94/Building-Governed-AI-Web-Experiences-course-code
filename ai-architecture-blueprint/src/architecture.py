from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class RecommendationDecision:
    title: str
    model_version: str
    evidence: Tuple[str, ...]
    explanation: str


@dataclass(frozen=True)
class MonitoringEvent:
    request_id: str
    model_version: str
    latency_ms: int
    outcome: str
    explanation_source: str


def explain_decision(
    title: str, requested_genre: str, candidate_genre: str
) -> str:
    if requested_genre == candidate_genre:
        return f"matched requested genre {requested_genre}"
    return "selected by catalog fallback"


def make_decision(
    title: str,
    model_version: str,
    requested_genre: str,
    candidate_genre: str,
) -> RecommendationDecision:
    explanation = explain_decision(title, requested_genre, candidate_genre)
    evidence = (f"requested_genre={requested_genre}", f"candidate_genre={candidate_genre}")
    return RecommendationDecision(title, model_version, evidence, explanation)


def record_event(
    decision: RecommendationDecision, request_id: str, latency_ms: int
) -> MonitoringEvent:
    return MonitoringEvent(
        request_id=request_id,
        model_version=decision.model_version,
        latency_ms=latency_ms,
        outcome=decision.title,
        explanation_source="decision_evidence",
    )


def choose_adaptation(latency_ms: int) -> str:
    if latency_ms >= 200:
        return "recommend_async_pipeline"
    return "keep_current_service"
