from src.evaluation import SAMPLE_RECORDS, evaluate


def test_sample_metrics():
    result = evaluate(SAMPLE_RECORDS)
    assert result["usefulness"] == 0.75
    assert result["accessibility_by_mode"] == {
        "keyboard": 0.5,
        "voice": 1.0,
        "screen_reader": 1.0,
    }
    assert result["harm_rate"] == 0.25
    assert result["correction_rate"] == 0.5


def test_empty_records_are_safe():
    assert evaluate([]) == {
        "usefulness": 0.0,
        "accessibility_by_mode": {},
        "harm_rate": 0.0,
        "correction_rate": 0.0,
    }
