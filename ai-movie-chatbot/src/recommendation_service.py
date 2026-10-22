MOVIES = [
    {"title": "The Mask", "genres": {"comedy"}},
    {"title": "Game Night", "genres": {"comedy"}},
    {"title": "Arrival", "genres": {"science fiction"}},
    {"title": "Moonlight", "genres": {"drama"}},
]


def recommend(preferences, watched, limit=3):
    """Return eligible titles with positive genre evidence."""
    wanted = set(preferences.get("genres", []))
    eligible = [movie for movie in MOVIES if movie["title"] not in watched]
    ranked = sorted(
        eligible,
        key=lambda movie: (-len(wanted & movie["genres"]), movie["title"]),
    )
    return [
        {
            "title": movie["title"],
            "evidence": sorted(wanted & movie["genres"]),
        }
        for movie in ranked
        if wanted & movie["genres"]
    ][:limit]


def recommend_from_state(dialogue_state):
    preferences = {"genres": [dialogue_state["genre"]]}
    watched = set(dialogue_state.get("exclude_watched", []))
    return recommend(preferences=preferences, watched=watched, limit=1)
