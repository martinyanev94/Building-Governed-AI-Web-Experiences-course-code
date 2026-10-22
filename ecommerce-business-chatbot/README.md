# Intelligent E-Commerce Business Chatbot

This project contains a controlled learning loop for chatbot evolution.

The loop accepts allowlisted feedback categories, creates a reviewable improvement proposal, compares a candidate with a baseline, blocks known regressions, and activates a new version only after approval.

## Run the tests

From this project directory:

```bash
python -m pytest
```

The module uses only the Python standard library at runtime. Tests require pytest.
