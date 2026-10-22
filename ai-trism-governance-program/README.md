# AI TRiSM governance program

This bounded Python prototype translates ethical principles into reviewable product requirements.

## Run

From the repository root:

```bash
python -m ai-trism-governance-program.src.governance
```

The module prints `True` when all defined requirements include affected groups, control text, evidence fields, and an owner.

If your Python environment does not accept the hyphenated module path, run:

```bash
python ai-trism-governance-program/src/governance.py
```

## Test

Install pytest if needed, then run:

```bash
pytest ai-trism-governance-program/tests
```

The tests verify the accountability boundary only. They do not establish production fairness, safety, security, or model quality.
