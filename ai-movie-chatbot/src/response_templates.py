def format_recommendation(results, requested_genre):
    if not results:
        return (
            f"I couldn't find an unwatched {requested_genre} "
            "movie in the current catalog."
        )

    result = results[0]
    evidence = ", ".join(result["evidence"])
    return (
        f"Try {result['title']}. It matches {evidence} "
        "and it isn't in your watched list."
    )
