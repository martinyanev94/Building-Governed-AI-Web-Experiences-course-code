"""Bounded commerce chatbot plan and operational instrumentation."""

ALLOWED_EVENTS = {
    "conversation_started",
    "order_status_viewed",
    "recommendation_clicked",
    "escalation_requested",
    "resolution_recorded",
}


def record_event(session_id, event_name, deployment_version, details=None):
    if event_name not in ALLOWED_EVENTS:
        raise ValueError("unsupported event")
    if not deployment_version:
        raise ValueError("deployment version is required")
    return {
        "session_id": session_id,
        "event_name": event_name,
        "deployment_version": deployment_version,
        "details": details or {},
    }


def handle_order_status(session_id, order_id, deployment_version, order_lookup):
    status = order_lookup(order_id)
    if status is None:
        event = record_event(
            session_id,
            "escalation_requested",
            deployment_version,
            {"reason": "order_not_found", "order_id": order_id},
        )
        return {
            "action": "escalate",
            "message": "A support specialist will help you.",
        }, event

    event = record_event(
        session_id,
        "order_status_viewed",
        deployment_version,
        {"order_id": order_id, "status": status},
    )
    return {
        "action": "answer",
        "message": f"Your order is {status}.",
    }, event


def deployment_record(version, channel, rollback_target):
    if not version or not channel or not rollback_target:
        raise ValueError("deployment record requires version, channel, and rollback")
    return {
        "version": version,
        "channel": channel,
        "rollback_target": rollback_target,
    }
