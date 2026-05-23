---
title: test-plan-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-review

Internal quality reviewer and auto-revision orchestrator. Scores test plans
against a 5-criteria rubric (specificity, grounding, scope fidelity, actionability,
consistency), each scored 0-2 for a 10-point scale. Uses forked score and review
agents, then enters a revision loop (max 2 cycles) where a revise agent edits
failing sections and re-scores. Writes TestPlanReview.md with scores, feedback,
and verdict (Ready/Revise/Rework).

**Plugin**: [test-plan](index.md) | **:material-close: Internal**

## Diagram

<div class="diagram-container" markdown>
![test-plan-review diagram](test-plan-review.svg)
</div>

## Usage

```bash
/test-plan-review
```
