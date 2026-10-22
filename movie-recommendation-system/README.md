# Movie recommendation prototype

A dependency-free Python prototype for preference-based movie recommendations with evidence-based rationales, explicit fallback reasons, and correction events.

## Run

From the project directory:

```bash
PYTHONPATH=. python src/main.py
```

## Test

Install pytest if needed, then run:

```bash
pytest
```

The rationale is generated from the current preference, recorded history, selected movie, and selection reason. Correction events preserve request context and do not mutate the preference profile.
