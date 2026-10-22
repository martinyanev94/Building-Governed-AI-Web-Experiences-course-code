from recommendation_feature import evaluate, recommend


if __name__ == "__main__":
    intent = "I need a quick vegetarian dinner"
    print("Recommendations:")
    for result in recommend(intent):
        print(f"- {result['title']}: score={result['score']}")

    cases = [
        ("vegetarian dinner", "vegetarian"),
        ("quick dinner", "quick"),
    ]
    print("Evaluation:")
    for result in evaluate(cases):
        print(result)
