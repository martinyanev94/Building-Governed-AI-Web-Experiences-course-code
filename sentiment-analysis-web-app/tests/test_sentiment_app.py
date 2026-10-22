import pytest

from src.sentiment_app import apply_review, classify_with_review


def test_mixed_evidence_requires_review():
    result = classify_with_review("The setup is clear, but the export fails")
    assert result["label"] == "uncertain"
    assert result["review_required"] is True
    assert result["state"] == "review_required"
    assert result["positive_evidence"] == ["clear"]
    assert result["negative_evidence"] == ["fails"]


def test_review_preserves_prediction_and_records_correction():
    result = classify_with_review("The support was friendly, but the refund is still missing")
    corrected = apply_review(result, "negative")
    assert corrected["state"] == "corrected"
    assert corrected["correction"] == {
        "from": "uncertain",
        "to": "negative",
        "evidence": ["friendly", "missing"],
    }


def test_unsupported_language_is_explicit():
    result = classify_with_review("La exportación falla", "es-ES")
    assert result["state"] == "language_unavailable"
    assert result["label"] is None


def test_unsupported_correction_is_rejected():
    result = classify_with_review("The setup is clear")
    with pytest.raises(ValueError):
        apply_review(result, "happy")
