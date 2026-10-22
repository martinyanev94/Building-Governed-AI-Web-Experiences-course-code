# AI Web Foundations Portfolio

This lesson adds a small, dependency-free portfolio assembly check. It connects four artifacts:

- prototype
- architecture
- tests
- governance

The portfolio is ready for review only when the artifact set and traceability links are complete, the feature remains advisory (`suggest_only`), and confirmation is required before consequential action.

## Run

From this directory:

```bash
python -m src.portfolio
python -m pytest
```

The module prints `ready_for_review` for the complete example. The tests also verify that unresolved automation and missing artifacts produce explicit hold decisions.
