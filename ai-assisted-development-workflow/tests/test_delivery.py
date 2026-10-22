from src.delivery import (
    ReviewRecord,
    TestEvidence,
    decide_release,
    record_monitoring,
    rollback_target,
)


def test_release_requires_risk_evidence_and_review():
    approved = ReviewRecord("Mina", True)
    assert decide_release(TestEvidence(True), approved).allowed
    assert not decide_release(TestEvidence(False), approved).allowed
    assert not decide_release(
        TestEvidence(True), ReviewRecord("Mina", False)
    ).allowed


def test_monitoring_preserves_version_and_outcome():
    assert record_monitoring("v2", "healthy") == {
        "version": "v2",
        "outcome": "healthy",
    }


def test_rollback_uses_previous_version_only_for_rollback_signal():
    assert rollback_target("v2", "rollback_required") == "v1"
    assert rollback_target("v2", "healthy") is None
