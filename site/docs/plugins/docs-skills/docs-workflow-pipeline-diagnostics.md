---
title: docs-workflow-pipeline-diagnostics
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-pipeline-diagnostics

Diagnoses a docs-orchestrator run for failures, bottlenecks, and
context-pressure risk. Runs `pipeline_diagnostics.py` over the progress file
and every step sidecar to produce structured JSON (summary, context
pressure, failures, bottlenecks, recommendations), then drills into each
failure by type, optionally analyzes a CI session log for error patterns and
compaction markers, and performs orchestrator self-introspection (schema
drift, missing sidecars, null results, stuck steps, step-order mismatches,
leftover active-workflow markers, timestamp gaps). Writes a full diagnostic
report plus a sidecar with counts and a context-pressure level (low/moderate/
high/critical).

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-pipeline-diagnostics diagram](docs-workflow-pipeline-diagnostics.svg)
</div>

## Arguments

```bash
/docs-workflow-pipeline-diagnostics <ticket> --base-path <path> [--ci-log <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads the progress file and all step sidecars). |
| `--ci-log` |  | - | Path to a CI session log for CI-specific analysis. |

## Usage

```bash
/docs-workflow-pipeline-diagnostics PROJ-123 --base-path .agent_workspace/proj-123
/docs-workflow-pipeline-diagnostics PROJ-123 --base-path .agent_workspace/proj-123 --ci-log ci.log
```
