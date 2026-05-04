<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-mlflow

Bidirectional MLflow sync. Syncs datasets, logs run results and metrics,
pushes judge scores and human feedback to execution traces.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-mlflow diagram](eval-mlflow.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--run-id` | :material-check: | — | Which eval run to sync |
| `--action` |  | `all` | Which sync action to perform |
| `--config` |  | `eval.yaml` | Path to eval config |

## Usage

```
/eval-mlflow --run-id 2026-05-01
/eval-mlflow --run-id latest --action sync-dataset
```
