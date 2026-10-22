# Personalized E-Commerce Recommendation System

The cold-start policy uses the content-based path when history is empty. It filters the catalog by the shopper's optional category and availability, then uses the first eligible item as a transparent fallback. It does not treat missing behavior as a negative preference.

A history-rich request uses the hybrid label only when content-signal evidence is also available. Otherwise it remains on the behavior-based path.

Evaluation records are grouped by request condition. The top-1 hit rate is the number of exact rank-one matches divided by evaluated cases. Later outcomes are evaluation labels, not inputs to the recommendation being evaluated.

From this directory, run:

PYTHONPATH=. python src/main.py
PYTHONPATH=. python -m pytest
