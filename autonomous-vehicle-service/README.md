# Autonomous vehicle service

A bounded Python prototype for modeling an autonomous vehicle as a machine customer.

The model records identity verification before authorization, separates permission
from station availability, routes unknown values to human review, supports explicit
operator approval or rejection, and preserves event reasons for terminal outcomes.
It is not production vehicle recognition, payment, fuel-control, or station software.

From this directory, run:

```bash
python -m pytest
```
