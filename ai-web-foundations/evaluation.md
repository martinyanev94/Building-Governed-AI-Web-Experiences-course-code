# Interface evaluation plan

This plan measures the recommendation interaction at the interface boundary.

## Event contract

The interface records task completion, input mode, corrections, and concrete observations such as keyboard navigation failure or an unavailable screen-reader action. A correction is diagnostic feedback. A reviewer sets `harmful` to true only when the recommendation is reviewed as unsuitable and the defined negative outcome occurred. Preference-only corrections remain non-harmful.

## Measures

- Usefulness: completed intended tasks divided by recorded interactions.
- Accessibility screening: task completion reported separately for each interaction mode, alongside observed accessibility barriers. Mode is a signal for investigation, not proof of cause.
- Unintended harm: reviewed harmful-event flags divided by recorded interactions.
- Diagnostic feedback: correction rate retained separately from the harm measure.

The records are illustrative until the team defines its event taxonomy, review thresholds, retention policy, and production collection process.

## Decision rule

Investigate any mode with materially lower completion than the others and inspect the concrete observations. Review harmful events individually. Use correction events to locate recommendation or interaction problems. Do not infer model quality from these interface measures alone.

## Run

From the `ai-web-foundations` directory:

```bash
python src/evaluation.py
pytest
```
