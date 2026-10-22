from src.decision import create_review_record, review_status


def test_review_status_accepts_only_explicit_approval():
    assert review_status("approved") == "approved"
    assert review_status("blocked") == "needs_changes"
    assert review_status("pending_review") == "needs_changes"
    assert review_status("") == "needs_changes"


def test_review_record_requires_verification():
    record = create_review_record(
        intent="guard assisted merge decision",
        files_changed=["src/decision.py"],
        tests_passed=False,
        risk_flags=[],
    )

    assert record.decision == "needs_changes"


def test_review_record_rejects_risk_flags():
    record = create_review_record(
        intent="guard assisted merge decision",
        files_changed=["src/decision.py"],
        tests_passed=True,
        risk_flags=["unknown status was approved"],
    )

    assert record.decision == "needs_changes"


def test_review_record_approves_verified_scoped_change():
    record = create_review_record(
        intent="guard assisted merge decision",
        files_changed=["src/decision.py"],
        tests_passed=True,
        risk_flags=[],
    )

    assert record.decision == "approved"
