import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from recommender import Product, rank_products


PRODUCTS = [
    Product("trail-shoes", "outdoor"),
    Product("rain-jacket", "outdoor"),
    Product("coffee-grinder", "kitchen"),
]


def test_excludes_already_purchased_products():
    result = rank_products(
        PRODUCTS,
        {"coffee-grinder": {"purchases": 1}},
        {"coffee-grinder"},
    )
    assert [item["product_id"] for item in result] == ["rain-jacket", "trail-shoes"]


def test_more_views_raise_a_product_in_the_ranking():
    preferences = {
        "trail-shoes": {"views": 2},
        "rain-jacket": {"views": 3},
    }
    result = rank_products(PRODUCTS[:2], preferences, set())
    assert [item["product_id"] for item in result] == ["rain-jacket", "trail-shoes"]


def test_empty_history_is_deterministic_and_eligible():
    result = rank_products(PRODUCTS[:2], {}, set())
    assert [item["product_id"] for item in result] == ["rain-jacket", "trail-shoes"]
    assert all(item["score"] == 0 for item in result)
