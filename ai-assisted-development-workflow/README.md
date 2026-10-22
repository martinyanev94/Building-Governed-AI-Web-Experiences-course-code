# AI-Augmented Software Development Workflow

This project models a small delivery workflow that joins risk-focused test evidence, human review, deployment gates, monitoring, and rollback selection.

## Run

From this directory, run:

```text
python -m pytest
```

The workflow is intentionally a bounded policy prototype. Its tests verify delivery contracts; they do not measure production recommendation quality or prove the safety of a deployed system.
