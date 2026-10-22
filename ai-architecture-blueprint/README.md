# Scalable AI Web Application Architecture

A standard-library Python prototype for an annotated AI architecture decision record.

## Run

From this directory, run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

The prototype demonstrates five boundaries: data, model, service, interface, and monitoring. It also records a model version, emits a structured monitoring event, selects a reviewable adaptation action, and explains a recommendation from recorded evidence.

The latency policy is an architecture example, not a production performance measurement: values at or above 200 milliseconds recommend reviewing an asynchronous pipeline.
