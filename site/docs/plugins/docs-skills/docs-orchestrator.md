---
title: docs-orchestrator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-orchestrator

The documentation pipeline orchestrator. Given a JIRA ticket, it reads an
ordered step list from `.agent_workspace/docs-workflow.yaml` (or a plugin
default), resolves the source code repository, and runs each step skill
sequentially — managing progress state in a JSON file, evaluating `when`
conditions, validating input dependencies, and handling resume. Claude is the
orchestrator; the YAML is a step list, not a workflow engine. It owns the
iteration loops (technical review up to 3 passes, quality gate up to 2
passes), the commit confirmation gate, and post-step processing. The default
workflow runs requirements → code-analysis → scope-req-audit → pr-analysis →
planning → writing → technical-review → style-review → security-review →
quality-gate → create-merge-request → pipeline-diagnostics, skipping
source-dependent steps automatically when no repo is found.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-orchestrator diagram](docs-orchestrator.svg)
</div>

## Arguments

```bash
/docs-orchestrator <ticket> [--workflow <name>] [--pr <url>]... [--source-code-repo <url-or-path>]... [--no-source-repo] [--auto-discover-repos] [--max-secondary-repos <N>] [--mkdocs] [--draft] [--docs-repo-path <path>] [--create-jira <PROJECT>] [--create-merge-request]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. If missing, the skill stops and asks. |
| `--workflow` |  | `docs-workflow` | Named workflow YAML variant to run. |
| `--pr` |  | - | PR/MR URL(s) to include; enables the pr-analysis step. Repeatable. |
| `--source-code-repo` |  | - | Source code repo URL or local path for code-aware steps. Repeatable. |
| `--no-source-repo` |  | `false` | Skip source resolution entirely; source-dependent steps are skipped. |
| `--auto-discover-repos` |  | `false` | Skip the secondary-repo confirmation prompt. |
| `--max-secondary-repos` |  | `3` | Maximum number of secondary repos to clone/index. |
| `--mkdocs` |  | `false` | Write Material for MkDocs Markdown instead of AsciiDoc. |
| `--draft` |  | `false` | Write to a staging area instead of updating docs in place. |
| `--docs-repo-path` |  | - | Target docs repository for update-in-place writing. |
| `--create-jira` |  | - | Create a linked JIRA ticket in the given project. |
| `--create-merge-request` |  | `false` | Open a merge request / pull request after reviews pass. |

## Usage

```bash
/docs-orchestrator PROJ-123
/docs-orchestrator PROJ-123 --pr https://github.com/org/repo/pull/42 --create-merge-request
/docs-orchestrator PROJ-123 --mkdocs --draft --no-source-repo
```
