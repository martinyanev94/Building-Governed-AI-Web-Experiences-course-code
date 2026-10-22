# Creative Generation Platform

A small Python prototype for a controlled AI-assisted creative workflow.

The workflow demonstrates:

- provenance attached to every generated draft;
- consent required before generation;
- explicit draft, approved, and rejected states;
- reviewer notes;
- submission blocked unless a draft is approved;
- regeneration linked to the rejected parent draft.

## Run the example

From this directory:

```bash
PYTHONPATH=. python src/main.py
```

## Run tests

```bash
PYTHONPATH=. python -m unittest discover -s tests
```

The generated content is deterministic placeholder text. It demonstrates workflow controls, not image or text model quality.
