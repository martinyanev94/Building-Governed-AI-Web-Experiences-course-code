from src.service_sequence import ServiceRequest, run_request


def states(events):
    return [event.state for event in events]


def test_approved_machine_customer_completes():
    request = ServiceRequest(
        "AV-204", "ST-07", "verified", "permitted", True
    )
    events = run_request(request)
    assert states(events) == [
        "requested", "identity_verified", "authorized",
        "servicing", "completed",
    ]
    assert events[-1].reason == "service_completed"


def test_unknown_permission_waits_for_operator():
    request = ServiceRequest(
        "AV-204", "ST-07", "verified", "unknown", True
    )
    events = run_request(request)
    assert states(events) == [
        "requested", "identity_verified", "human_review"
    ]
    assert events[-1].reason == "permission_unknown"


def test_operator_approval_continues_review():
    request = ServiceRequest(
        "AV-204", "ST-07", "verified", "unknown", True
    )
    events = run_request(request, operator_decision="approve")
    assert states(events)[-3:] == ["servicing", "completed"][-2:]
    assert events[2].reason == "permission_unknown"
    assert events[3].reason == "human_approved"


def test_operator_rejection_stops_review():
    request = ServiceRequest(
        "AV-204", "ST-07", "verified", "unknown", True
    )
    events = run_request(request, operator_decision="reject")
    assert states(events) == [
        "requested", "identity_verified", "human_review", "rejected"
    ]
    assert events[-1].reason == "human_rejected"


def test_rejection_reasons_remain_distinct():
    denied = ServiceRequest("AV-204", "ST-07", "verified", "denied", True)
    unavailable = ServiceRequest("AV-204", "ST-07", "verified", "permitted", False)
    assert run_request(denied)[-1].reason == "permission_denied"
    assert run_request(unavailable)[-1].reason == "station_unavailable"
