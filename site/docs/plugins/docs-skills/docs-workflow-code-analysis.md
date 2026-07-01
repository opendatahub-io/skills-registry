---
title: docs-workflow-code-analysis
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-code-analysis

Orchestrator step that wraps `learn-code` to analyze a source repository and
produce structured code understanding (ONBOARDING.md, module registry,
per-module summaries, cross-module relationships) for downstream steps. Runs
learn-code inside an isolated subagent to keep 850+ lines of skill text and
intermediate orchestration out of the main context, checks for cached
analysis in both in-repo and docs-repo `.agent_workspace/` locations, copies
results into the step output dir, and writes a sidecar with module/
relationship counts and detected languages. Conditional on `has_source_repo`.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-code-analysis diagram](docs-workflow-code-analysis.svg)
</div>

## Arguments

```bash
/docs-workflow-code-analysis --repo <path> --ticket <TICKET> --output-dir <path>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--repo` | :material-check: | - | Path to the cloned source repository. |
| `--ticket` | :material-check: | - | JIRA ticket ID. |
| `--output-dir` | :material-check: | - | Base output directory (.agent_workspace/<ticket>/code-analysis/). |

## Usage

```bash
/docs-workflow-code-analysis --repo /path/to/repo --ticket PROJ-123 --output-dir .agent_workspace/proj-123/code-analysis
```
