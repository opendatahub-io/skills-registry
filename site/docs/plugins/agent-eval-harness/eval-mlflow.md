---
title: eval-mlflow
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-mlflow

Bidirectional MLflow integration for evaluation results, datasets, and
feedback. Syncs test cases to MLflow dataset registry with a schema mapping
you define (inputs vs expectations), logs run params/metrics/artifacts/traces
to MLflow experiments, pushes judge scores and human feedback to execution
traces, and pulls annotations added via the MLflow UI back into review.yaml
for /eval-optimize to consume. Resolves tracking URI from eval.yaml, then
MLFLOW_TRACKING_URI env var, then defaults to localhost:5000.

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
| `--config` |  | `eval.yaml` | Path to eval config. |

## Usage

```bash
/eval-mlflow --run-id 2026-05-01-opus
/eval-mlflow --action sync-dataset
/eval-mlflow --run-id 2026-05-01-opus --action push-feedback
```
