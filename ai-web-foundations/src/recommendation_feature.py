RECIPES = [
    {"title": "Green lentil bowl", "tags": {"vegetarian", "dinner"}},
    {"title": "Chicken rice bowl", "tags": {"quick", "dinner"}},
    {"title": "Mushroom pasta", "tags": {"vegetarian", "dinner"}},
]


def recommend(user_intent, recipes=RECIPES):
    terms = {word.lower().strip(".,?!") for word in user_intent.split()}
    ranked = []
    for recipe in recipes:
        score = len(terms & recipe["tags"])
        ranked.append({"title": recipe["title"], "score": score})
    return sorted(ranked, key=lambda item: item["score"], reverse=True)


def evaluate(cases, recipes=RECIPES):
    results = []
    for user_intent, expected_tag in cases:
        ranked = recommend(user_intent, recipes)
        if not ranked:
            results.append({
                "input": user_intent,
                "top_title": None,
                "score": 0,
                "hit": False,
            })
            continue
        top_match = ranked[0]
        top_recipe = next(
            (recipe for recipe in recipes
             if recipe["title"] == top_match["title"]),
            None,
        )
        results.append({
            "input": user_intent,
            "top_title": top_match["title"],
            "score": top_match["score"],
            "hit": top_recipe is not None
            and expected_tag in top_recipe["tags"],
        })
    return results
