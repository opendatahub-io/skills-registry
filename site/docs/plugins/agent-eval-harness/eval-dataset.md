---
title: eval-dataset
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-dataset

Generates realistic test cases based on the eval.yaml dataset schema and
judge criteria. Supports three strategies: bootstrap (from scratch with
simple/complex/edge case coverage), expand (fills gaps in existing datasets
by analyzing what judges check that no case tests), and from-traces (extracts
real inputs from MLflow production traces). Handles external-state fields
with TODO_ placeholders, generates answers.yaml for interactive skills using
AskUserQuestion, and creates annotations.yaml for outcome-aware judges.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-dataset diagram](eval-dataset.svg)
</div>

## Arguments

```bash
/eval-dataset [--config <path>] [--count <N>] [--strategy <type>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--config` |  | `eval.yaml` | Path to eval config. |
| `--count` |  | `5` | Number of test cases to generate. |
| `--strategy` |  | `bootstrap` | Generation strategy. bootstrap: from scratch. expand: fill gaps in existing dataset. from-traces: extract from MLflow traces. |

## Usage

```bash
/eval-dataset
/eval-dataset --count 10 --strategy expand
/eval-dataset --strategy from-traces
```
