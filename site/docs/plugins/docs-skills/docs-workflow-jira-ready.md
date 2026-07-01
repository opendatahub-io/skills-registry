---
title: docs-workflow-jira-ready
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-jira-ready

A check-and-return gate for automated docs-orchestrator runs. Queries JIRA
via `jira_reader.py` (fast summary mode), filters out tickets that already
have a workflow progress file or the `docs-workflow-started` label, and
outputs a JSON list of actionable ticket IDs. It does NOT dispatch the
orchestrator — the caller (cron, CI, or a human) decides what to do with the
list. With `--add-label` it stamps the returned tickets so they don't
reappear on the next run. Designed as the entry point for scheduled or
CI-triggered documentation automation.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-jira-ready diagram](docs-workflow-jira-ready.svg)
</div>

## Arguments

```bash
/docs-workflow-jira-ready --jql <query> [--base-path <path>] [--label <label>] [--add-label] [--max-results <n>] [--dry-run]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--jql` | :material-check: | - | JQL query string (quote it). |
| `--base-path` |  | `artifacts` | Directory checked for existing workflow progress files. |
| `--label` |  | `docs-workflow-started` | JIRA label marking a ticket as already started. |
| `--add-label` |  | `false` | Add the tracking label to each returned ticket in JIRA. |
| `--max-results` |  | `5` | Maximum number of JIRA results to fetch. |
| `--dry-run` |  | `true` | Report results with no side effects (default behavior). |

## Usage

```bash
/docs-workflow-jira-ready --jql "project=PROJ AND labels=docs-needed"
/docs-workflow-jira-ready --jql "project=PROJ AND labels=docs-needed" --add-label
```
