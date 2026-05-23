---
title: rfe.auto-fix
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.auto-fix

Non-interactive batch pipeline for reviewing, revising, and splitting
RFEs at scale. Accepts explicit IDs or a JQL query to fetch from Jira.
Uses a pipeline state machine (pipeline_state.py) with phased dispatch:
fetch, bootstrap, assess, feasibility, review, revise, re-assess, and
split. Processes in configurable batch sizes with resume support via
snapshot-based incremental fetch. Supports reprocessing previously
handled RFEs and random sampling.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.auto-fix diagram](rfe.auto-fix.svg)
</div>

## Arguments

```bash
/rfe.auto-fix <IDs...> | --jql <query> [--limit N] [--batch-size N] [--headless] [--reprocess] [--random N] [--announce-complete] [--data-dir <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `IDs` |  | - | Explicit RFE IDs to process (space-separated) |
| `--jql` |  | - | JQL query to fetch RFE IDs from Jira |
| `--limit` |  | - | Max number of results from JQL query |
| `--batch-size` |  | `50` | Process IDs in batches of this size |
| `--data-dir` |  | - | Directory for snapshot data |
| `--headless` |  | - | Non-interactive mode |
| `--reprocess` |  | - | Reprocess RFEs that had prior runs |
| `--random` |  | - | Process N random RFEs from the result set |
| `--announce-complete` |  | - | Print completion marker when done |

## Usage

```bash
/rfe.auto-fix RFE-001 RFE-002 RFE-003
/rfe.auto-fix --jql "project=RHAIRFE AND status=New" --limit 20
/rfe.auto-fix --jql "project=RHAIRFE" --reprocess --random 5
```
