# Regulated AI Management Framework

This lesson extends the requirements map into a reviewable operating cycle.

## Run the demonstration

From this directory:

```bash
python -m src.framework_map
```

## Run tests

```bash
python -m unittest discover -s tests
```

The workflow treats a requirement as reviewable only when it is marked present
and has an evidence reference. The review records its objective and whether the
criteria were met. Missing evidence produces an escalation with a reason, an
owner, and a next review date. An immutable evidence update is checked in the
next cycle. This is an operational record, not a legal compliance conclusion.
