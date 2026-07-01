---
title: docs-workflow-scope-req-audit
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-scope-req-audit

Classifies each JIRA requirement as grounded, partial, or absent by code
evidence before planning, preventing hallucinated documentation for
unimplemented features. Discovers related repos from README/docs, loads (or
runs) learn-code analysis, then fans out one classifier subagent per
requirement — each reads analysis data from disk and inspects the actual
source with Read/Grep/Glob, writing a per-requirement JSON classification. A
merge agent assembles evidence-status.json and summary.md, and a secondary
script extracts companion repos referenced in gap actions. Planning then
gives grounded requirements full specs, flags partial ones for SME review,
and defers absent ones. Conditional on `has_source_repo`.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-scope-req-audit diagram](docs-workflow-scope-req-audit.svg)
</div>

## Arguments

```bash
/docs-workflow-scope-req-audit <ticket> --base-path <path> --repo <path>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads requirements/requirements.md). |
| `--repo` | :material-check: | - | Path to the source code repository (provided by the orchestrator). |

## Usage

```bash
/docs-workflow-scope-req-audit PROJ-123 --base-path .agent_workspace/proj-123 --repo /path/to/repo
```
