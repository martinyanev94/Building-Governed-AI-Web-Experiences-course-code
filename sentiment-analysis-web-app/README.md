# Sentiment Analysis Web Application

This bounded Python prototype connects sentiment evidence to review, correction, and language-aware interface states.

## Run

From the project directory:

```bash
python src/sentiment_app.py
```

## Test

Install pytest if needed, then run:

```bash
python -m pytest
```

The prototype supports `en-US`. Mixed or absent sentiment evidence produces `review_required`; unsupported languages produce `language_unavailable`. Human corrections preserve the original prediction and record the evidence used.
