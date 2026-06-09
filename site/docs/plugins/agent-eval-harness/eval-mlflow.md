---
title: eval-mlflow
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-mlflow

Bidirectional MLflow integration for evaluation results, datasets, and
feedback. Syncs test cases to the MLflow dataset registry using a two-phase
flow where you produce a schema_mapping.json (inputs vs expectations, mapping
record fields to source files/field paths) and a script syncs deterministically;
logs run params, metrics, artifacts, per-case results tables, and traces to
MLflow experiments; pushes judge scores (source_type=CODE) and human feedback
(source_type=HUMAN) to execution traces; and pulls annotations added via the
MLflow UI back into review.yaml (under mlflow_feedback) for /eval-optimize to
consume. Resolves tracking URI from mlflow.tracking_uri in eval.yaml, then the
MLFLOW_TRACKING_URI env var, then defaults to http://127.0.0.1:5000. Degrades
gracefully -- if MLflow is unavailable, scripts exit cleanly and the skill
reports that it was skipped.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-mlflow diagram](eval-mlflow.svg)
</div>

## Arguments

```bash
/eval-mlflow [--action <action>] [--run-id <id>] [--config <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--action` |  | `all` | Which sync action to perform. |
| `--run-id` |  | - | Which eval run to log or attach feedback to. Required for log-results, push-feedback, and pull-feedback. |
| `--config` |  | `auto-discover` | Path to eval config. |

## Usage

```bash
/eval-mlflow --run-id 2026-05-01-opus
/eval-mlflow --action sync-dataset
/eval-mlflow --run-id 2026-05-01-opus --action push-feedback
```
