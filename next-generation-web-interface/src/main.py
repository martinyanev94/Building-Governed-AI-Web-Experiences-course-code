import json

from compare_approaches import design_interaction


examples = [
    design_interaction(
        "conversational",
        "What am I looking at?",
        "Sculpture Hall",
    ),
    design_interaction(
        "ar",
        "Show the sculpture",
        "Sculpture Hall",
        has_camera=True,
        consent=False,
    ),
]

for example in examples:
    print(json.dumps(example))
