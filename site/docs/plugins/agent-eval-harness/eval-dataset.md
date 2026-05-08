---
title: eval-dataset
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-dataset

Generate realistic test cases from the eval.yaml schema. Supports bootstrap
(from scratch), expand (fill gaps), and from-traces (extract from MLflow) strategies.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-dataset diagram](eval-dataset.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--count` |  | `3` | Number of test cases to generate |
| `--strategy` |  | `auto` | Generation strategy |
| `--config` |  | `eval.yaml` | Path to eval config |

## Usage

```
/eval-dataset
/eval-dataset --count 5 --strategy expand
/eval-dataset --strategy from-traces
```
