---
title: docs-workflow-style-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-style-review

Orchestrator step for style-guide compliance review of the documentation
drafts. Determines the source files from the writing sidecar and dispatches
the `docs-reviewer` subagent, which runs Vale linting once per file, fixes
unambiguous errors, and applies the full battery of review skills — modular
docs and content quality plus the eight IBM Style Guide and eight Red Hat SSG
checkers (release-notes and modular-docs are skipped for MkDocs). Edits files
in place and writes the review report plus a sidecar.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-style-review diagram](docs-workflow-style-review.svg)
</div>

## Arguments

```bash
/docs-workflow-style-review <ticket> --base-path <path> --format <adoc|mkdocs>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads writing/ output). |
| `--format` |  | `adoc` | Documentation format (selects which review skills apply). |

## Usage

```bash
/docs-workflow-style-review PROJ-123 --base-path .agent_workspace/proj-123 --format adoc
```
