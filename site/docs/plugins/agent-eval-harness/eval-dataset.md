---
title: eval-dataset
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-dataset

Generates realistic test cases based on the eval.yaml dataset schema and
judge criteria. Reads eval.md and eval.yaml to derive judge-driven
requirements (each case should exercise at least one judge criterion), then
generates cases via one of three strategies: bootstrap (from scratch with
simple/complex/edge case coverage), expand (fills gaps in existing datasets
by analyzing what judges check that no case tests, optionally learning from a
previous run's failure patterns), and from-traces (extracts real inputs from
MLflow production traces). Handles external-state fields with TODO_
placeholders (so it never fabricates Jira keys, repos, or API endpoints),
generates answers.yaml guidance for interactive skills using AskUserQuestion,
and creates annotations.yaml for outcome-aware judges (ensuring conditional
judges are exercised on both branches). Can invoke /eval-analyze first when
no config exists.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-dataset diagram](eval-dataset.svg)
</div>

## Arguments

```bash
/eval-dataset [--config <path>] [--count <N>] [--strategy <type>] [--run-id <id>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--config` |  | `auto-discover` | Path to eval config. |
| `--count` |  | `5` | Number of test cases to generate. |
| `--strategy` |  | `bootstrap` | Generation strategy. bootstrap: from scratch. expand: fill gaps in existing dataset. from-traces: extract from MLflow traces (falls back to expand if none found). |
| `--run-id` |  | - | Previous eval run to learn from when filling coverage gaps (used with the expand strategy to target empirical failure patterns). |

## Usage

```bash
/eval-dataset
/eval-dataset --count 10 --strategy expand
/eval-dataset --strategy from-traces
```
