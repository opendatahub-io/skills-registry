---
title: docs-workflow-pr-analysis
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-pr-analysis

Orchestrator step that wraps `understand-pull-request` to analyze a specific
PR/MR and produce change-specific documentation context. Runs the analysis
inside an isolated subagent (keeping 570+ lines of skill text out of the main
context), reuses any prior `code-analysis` for richer module context, copies
the resulting PR-ANALYSIS.md into the step output dir, and writes a sidecar
with PR number, modules-affected count, and platform. Conditional on
`has_pr` — skipped when no PR URL is available.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-pr-analysis diagram](docs-workflow-pr-analysis.svg)
</div>

## Arguments

```bash
/docs-workflow-pr-analysis --pr <url> --repo <path> --ticket <TICKET> --output-dir <path>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--pr` | :material-check: | - | PR/MR URL (GitHub or GitLab). |
| `--repo` | :material-check: | - | Path to the cloned source repository. |
| `--ticket` | :material-check: | - | JIRA ticket ID. |
| `--output-dir` | :material-check: | - | Base output directory (.agent_workspace/<ticket>/pr-analysis/). |

## Usage

```bash
/docs-workflow-pr-analysis --pr https://github.com/org/repo/pull/42 --repo /path/to/repo --ticket PROJ-123 --output-dir .agent_workspace/proj-123/pr-analysis
```
