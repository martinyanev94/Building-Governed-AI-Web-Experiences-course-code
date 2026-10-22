from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Product:
    product_id: str
    category: str


def score_product(product: Product, preferences: dict[str, dict[str, int]]) -> dict[str, Any]:
    signal = preferences.get(product.product_id, {})
    score = 2 * signal.get("views", 0) + 5 * signal.get("purchases", 0)
    return {
        "product_id": product.product_id,
        "category": product.category,
        "score": score,
        "evidence": {
            "views": signal.get("views", 0),
            "purchases": signal.get("purchases", 0),
        },
    }


def rank_products(
    products: list[Product],
    preferences: dict[str, dict[str, int]],
    purchased_ids: set[str],
    limit: int = 3,
) -> list[dict[str, Any]]:
    ranked = []
    for product in products:
        if product.product_id in purchased_ids:
            continue
        ranked.append(score_product(product, preferences))

    return sorted(
        ranked,
        key=lambda item: (-item["score"], item["product_id"]),
    )[:limit]
