from src.auth_design import evaluate_visual_auth


def test_verified_result_still_returns_authorization_boundary():
    result = evaluate_visual_auth("verified", True, True, False)
    assert result.state == "verified"
    assert result.message == "Continue to authorization."
    assert result.audit_event == "visual_verified"
    assert result.retained_image is False


def test_uncertain_result_uses_fallback():
    result = evaluate_visual_auth("uncertain", True, True, False)
    assert result.state == "uncertain"
    assert result.message == "Use another sign-in method."
    assert result.audit_event == "visual_uncertain"
    assert result.retained_image is False


def test_preprocessing_failure_does_not_verify():
    result = evaluate_visual_auth("verified", True, False, False)
    assert result.state == "fallback"
    assert result.audit_event == "preprocessing_failed"
    assert result.retained_image is False


def test_camera_unavailable_has_non_visual_path():
    result = evaluate_visual_auth("verified", False, True, False)
    assert result.state == "fallback"
    assert result.message == "Use another sign-in method."
    assert result.audit_event == "camera_unavailable"
    assert result.retained_image is False


def test_retention_request_cannot_change_privacy_boundary():
    result = evaluate_visual_auth("verified", True, True, True)
    assert result.state == "uncertain"
    assert result.retained_image is False
