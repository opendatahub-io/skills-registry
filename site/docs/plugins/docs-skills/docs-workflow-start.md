---
title: docs-workflow-start
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-start

The interactive entry point for the documentation workflow. With no `--`
switches, it walks the user through AskUserQuestion steps — ticket ID, action
(full workflow / specific steps / resume), output format, source-code
availability, placement, and JIRA creation — then builds the CLI flags and
hands off to `docs-orchestrator`. In specific-steps mode it resolves
prerequisites via `resolve_steps.py`, validates `requires`/`when` conditions,
offers to reuse existing artifacts, and runs the selected steps directly.
When switches are already present it passes straight through to the
orchestrator with no prompts. Invoke this only on explicit request — for
`docs-orchestrator`, that skill runs directly.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-start diagram](docs-workflow-start.svg)
</div>

## Arguments

```bash
/docs-workflow-start [<ticket>] [--workflow <name>] [--pr <url>]... [--source-code-repo <url-or-path>]... [--no-source-repo] [--auto-discover-repos] [--max-secondary-repos <N>] [--mkdocs] [--draft] [--docs-repo-path <path>] [--create-jira <PROJECT>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` |  | - | JIRA ticket ID (asked interactively if omitted). |
| `--... (switches)` |  | - | Any docs-orchestrator switch. If any switch is present, this skill passes through to the orchestrator without prompting. |

## Usage

```bash
/docs-workflow-start
/docs-workflow-start PROJ-123
/docs-workflow-start PROJ-123 --mkdocs --draft
```
