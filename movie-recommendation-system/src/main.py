from movie_recommender import build_response, record_correction


def main() -> None:
    preference = "science fiction"
    history = {"Arrival": "science fiction", "Dune": "science fiction"}
    catalog = {
        "Solaris": "science fiction",
        "Amelie": "comedy",
    }
    watched = {"Arrival", "Dune"}

    response = build_response(preference, history, catalog, watched)
    print(response)

    correction = record_correction(
        response["movie"],
        "not_relevant",
        preference,
        history,
        watched,
        "preference_match",
    )
    print(correction)


if __name__ == "__main__":
    main()
