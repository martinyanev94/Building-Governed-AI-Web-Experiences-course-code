from __future__ import annotations

POSITIVE = {"clear", "friendly", "good", "great", "helpful", "love", "smooth"}
NEGATIVE = {"bad", "broken", "fail", "fails", "missing", "poor", "slow"}
SUPPORTED_LANGUAGES = {"en-US"}


def classify_sentiment(text: str) -> dict:
    tokens = [token.strip(".,!?;:").lower() for token in text.split()]
    positive = [token for token in tokens if token in POSITIVE]
    negative = [token for token in tokens if token in NEGATIVE]
    if positive and not negative:
        label = "positive"
    elif negative and not positive:
        label = "negative"
    elif positive or negative:
        label = "uncertain"
    else:
        label = "uncertain"
    return {
        "label": label,
        "positive_evidence": positive,
        "negative_evidence": negative,
    }


def classify_with_review(text: str, language: str = "en-US") -> dict:
    if language not in SUPPORTED_LANGUAGES:
        return {
            "text": text,
            "language": language,
            "label": None,
            "positive_evidence": [],
            "negative_evidence": [],
            "review_required": False,
            "state": "language_unavailable",
        }
    result = classify_sentiment(text)
    mixed = bool(result["positive_evidence"]) and bool(result["negative_evidence"])
    needs_review = result["label"] == "uncertain" or mixed
    return {
        "text": text,
        **result,
        "language": language,
        "review_required": needs_review,
        "state": "review_required" if needs_review else "automatic",
    }


def apply_review(response: dict, corrected_label: str) -> dict:
    allowed = {"positive", "negative", "neutral"}
    if corrected_label not in allowed:
        raise ValueError("unsupported correction label")
    evidence = response["positive_evidence"] + response["negative_evidence"]
    return {
        **response,
        "label": corrected_label,
        "state": "corrected",
        "correction": {
            "from": response["label"],
            "to": corrected_label,
            "evidence": evidence,
        },
    }


if __name__ == "__main__":
    response = classify_with_review("The setup is clear, but the export fails")
    print(response)
    print(apply_review(response, "negative"))
