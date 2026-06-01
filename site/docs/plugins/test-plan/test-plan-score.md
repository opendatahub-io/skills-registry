---
title: test-plan-score
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-score

Score an existing test plan using the 5-criteria quality rubric (Specificity,
Grounding, Scope Fidelity, Actionability, Consistency) without triggering
auto-revision. Read-only assessment for standalone quality evaluation or
evaluating test plans created outside the automated pipeline.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-score diagram](test-plan-score.svg)
</div>

## Arguments

```bash
/test-plan-score <feature_dir>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `feature_dir` | :material-check: | - | Path to directory containing TestPlan.md |

## Usage

```bash
/test-plan-score kagenti_agent_templates
/test-plan-score mcp_catalog
```
