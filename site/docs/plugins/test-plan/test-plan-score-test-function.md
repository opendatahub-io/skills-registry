---
title: test-plan-score-test-function
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-score-test-function

Internal forked scorer sub-agent. Evaluates generated test function code using a
5-criteria rubric: Coverage (all TC requirements implemented), Assertions (specific
and meaningful), Convention Adherence (follows repo patterns), Test Data (realistic
values from TC), Code Quality (clean, no excessive TODOs). Returns verdict
(Ready/Good/Revise/Rework) with per-criterion scores and revision recommendations.

**Plugin**: [test-plan](index.md) | **:material-close: Internal**

## Diagram

<div class="diagram-container" markdown>
![test-plan-score-test-function diagram](test-plan-score-test-function.svg)
</div>

## Usage

```bash
/test-plan-score-test-function
```
