---
title: docs-workflow-writing
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-writing

Orchestrator step that writes documentation from the plan by dispatching the
`docs-writer` subagent. A build script parses arguments, validates inputs,
determines the mode (update-in-place / draft / fix) and format
(AsciiDoc / MkDocs), and resolves code-analysis, PR-analysis, and repo paths.
The agent writes the docs and a manifest; the step then records the produced
file paths in a sidecar (skipped in fix mode, which edits in place). Default
placement is update-in-place; `--draft` stages to the workspace; `--fix-from`
applies review corrections.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-writing diagram](docs-workflow-writing.svg)
</div>

## Arguments

```bash
/docs-workflow-writing <ticket> --base-path <path> --format <adoc|mkdocs> [--draft] [--repo <path>]... [--repo-path <path>] [--fix-from <review_path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads planning/plan.md). |
| `--format` |  | `adoc` | Output documentation format. |
| `--draft` |  | `false` | Write to the staging area instead of updating in place. |
| `--repo` |  | - | Source code repo path(s) for grounding. Repeatable. |
| `--repo-path` |  | - | Target docs repository for update-in-place output. |
| `--fix-from` |  | - | Apply corrections from a review/feedback file (fix mode). |

## Usage

```bash
/docs-workflow-writing PROJ-123 --base-path .agent_workspace/proj-123 --format adoc
/docs-workflow-writing PROJ-123 --base-path .agent_workspace/proj-123 --format mkdocs --draft
```
