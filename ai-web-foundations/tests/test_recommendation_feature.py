import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from recommendation_feature import evaluate, recommend


def test_vegetarian_dinner_has_a_top_match():
    results = recommend("vegetarian dinner")
    assert results[0]["title"] == "Green lentil bowl"
    assert results[0]["score"] == 2


def test_evaluation_records_a_hit():
    results = evaluate([("vegetarian dinner", "vegetarian")])
    assert results == [
        {
            "input": "vegetarian dinner",
            "top_title": "Green lentil bowl",
            "score": 2,
            "hit": True,
        }
    ]
