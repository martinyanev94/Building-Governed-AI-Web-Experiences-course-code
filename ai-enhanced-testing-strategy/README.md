# AI-Enhanced Testing Strategy

A standard-library Python artifact for prioritizing tests across performance, security, bias, reliability, and validity risks.

## Run

From this directory:

```bash
python -m unittest discover -s tests -v
python -m src.testing_strategy
```

The strategy uses impact multiplied by likelihood, then breaks equal-priority ties by test name. The scores are explicit assumptions for review, not production measurements or proof of model quality.
