---
title: eval-setup
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-setup

Optional, non-destructive environment configurator for the evaluation
harness. Installs dependencies into the isolated venv (as a fallback for
mid-session installs or troubleshooting), configures MLflow tracking (local
server, local file store, or remote/Databricks), verifies API keys
(Anthropic API or Vertex AI), sets up the runs directory, checks
skill-specific environment variables referenced in eval.yaml's
execution.env, and creates the MLflow experiment. Runs check_env.py
preflight checks (with --fix) and re-verifies at the end. Most users can
skip this -- dependencies auto-install via the plugin's SessionStart hook
and agent_eval is available via symlinks.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-setup diagram](eval-setup.svg)
</div>

## Arguments

```bash
/eval-setup [--tracking-uri <uri>] [--skip-mlflow] [--runs-dir <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--tracking-uri` |  | `auto-detect` | MLflow tracking URI (skips interactive setup). Accepts local or remote URIs. |
| `--skip-mlflow` |  | `false` | Skip MLflow setup entirely. The harness works without MLflow. |
| `--runs-dir` |  | `eval/runs` | Directory where eval runs are stored. Configured via AGENT_EVAL_RUNS_DIR env var. |

## Usage

```bash
/eval-setup
/eval-setup --tracking-uri http://127.0.0.1:5000
/eval-setup --skip-mlflow
```
