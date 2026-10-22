from __future__ import annotations

from typing import Any


def recommend_with_reason(
    preference: str,
    history: dict[str, str],
    catalog: dict[str, str],
    watched: set[str],
) -> tuple[str, str]:
    eligible = sorted(
        title
        for title, genre in catalog.items()
        if title not in watched and genre == preference
    )
    if eligible:
        return eligible[0], "preference_match"

    fallback = sorted(title for title in catalog if title not in watched)
    if not fallback:
        raise LookupError("no unwatched movies available")
    return fallback[0], "catalog_fallback"


def recommend(
    preference: str,
    history: dict[str, str],
    catalog: dict[str, str],
    watched: set[str],
) -> str:
    selected, _ = recommend_with_reason(preference, history, catalog, watched)
    return selected


def build_rationale(
    preference: str,
    history: dict[str, str],
    selected: str,
    selection_reason: str,
) -> str:
    matching_history = [
        title for title, genre in history.items()
        if genre == preference
    ]
    if selection_reason == "catalog_fallback":
        return (
            f"Recommended {selected} as a catalog fallback because "
            f"no unwatched {preference} movie was available."
        )

    rationale = (
        f"Recommended {selected} because you selected {preference}"
    )
    if matching_history:
        rationale += f" and your history includes {preference} movies"
    return rationale + "."


def record_correction(
    selected: str,
    correction: str,
    preference: str,
    history: dict[str, str],
    watched: set[str],
    selection_reason: str,
) -> dict[str, Any]:
    allowed = {"not_relevant", "more_like_this"}
    if correction not in allowed:
        raise ValueError("unsupported correction")
    return {
        "movie": selected,
        "correction": correction,
        "preference_at_request": preference,
        "history": dict(history),
        "watched": sorted(watched),
        "selection_reason": selection_reason,
    }


def build_response(
    preference: str,
    history: dict[str, str],
    catalog: dict[str, str],
    watched: set[str],
) -> dict[str, str]:
    selected, reason = recommend_with_reason(
        preference, history, catalog, watched
    )
    return {
        "movie": selected,
        "rationale": build_rationale(
            preference, history, selected, reason
        ),
        "correction": "not_relevant",
    }
