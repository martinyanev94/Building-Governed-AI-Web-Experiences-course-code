from src.commerce_chatbot_plan import (
    deployment_record,
    handle_order_status,
    record_event,
)


def test_successful_lookup_records_view_event():
    response, event = handle_order_status(
        "s-23", "O-52", "0.3", lambda _order_id: "shipped"
    )
    assert response == {"action": "answer", "message": "Your order is shipped."}
    assert event["event_name"] == "order_status_viewed"
    assert event["details"] == {"order_id": "O-52", "status": "shipped"}
    assert event["deployment_version"] == "0.3"


def test_missing_order_escalates_without_inventing_status():
    response, event = handle_order_status(
        "s-22", "O-51", "0.3", lambda _order_id: None
    )
    assert response["action"] == "escalate"
    assert event["event_name"] == "escalation_requested"
    assert event["details"] == {
        "reason": "order_not_found",
        "order_id": "O-51",
    }
    assert event["deployment_version"] == "0.3"


def test_unknown_event_fails_closed():
    try:
        record_event("s-22", "made_up_event", "0.3")
    except ValueError as error:
        assert str(error) == "unsupported event"
    else:
        raise AssertionError("unknown event must fail closed")


def test_deployment_record_requires_rollback_target():
    record = deployment_record("0.3", "web", "0.2")
    assert record["rollback_target"] == "0.2"
