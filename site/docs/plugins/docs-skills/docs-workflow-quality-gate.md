---
title: docs-workflow-quality-gate
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-quality-gate

Scores the pipeline's documentation output before a merge request is opened.
Prepares judge prompts, runs a per-AC coverage check (one subagent per
acceptance-criterion, each verifying coverage with a verbatim supporting
quote), then dispatches two Opus judge agents in parallel — doc_quality and
intent_alignment — returning structured scores via schema validation. Gaps
are classified against scope-req-audit evidence (absent →
document-as-unsupported, partial → expand-with-evidence, grounded →
add-missing-section) and, when the gate fails, written into an
iteration-numbered feedback brief the orchestrator feeds to the writer in fix
mode. Passing requires intent_alignment >= 4; iteration logic lives in the
orchestrator. Conditional on `has_many_requirements`.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-quality-gate diagram](docs-workflow-quality-gate.svg)
</div>

## Arguments

```bash
/docs-workflow-quality-gate <ticket> --base-path <path>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads writing output, requirements discovery, and evidence status). |

## Usage

```bash
/docs-workflow-quality-gate PROJ-123 --base-path .agent_workspace/proj-123
```
