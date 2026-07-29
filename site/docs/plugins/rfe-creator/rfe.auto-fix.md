---
title: rfe.auto-fix
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.auto-fix

Non-interactive batch pipeline for reviewing, revising, and splitting RFEs
at scale. Accepts explicit IDs or a JQL query (with --limit and --random
sampling) to fetch from Jira. Runs a pipeline state machine
(pipeline_state.py) with phased dispatch -- fetch, bootstrap, assess,
feasibility, review, revise, re-assess, and split -- driven by a strict
next-action / launch_wave / wait-for-wave loop that must run to completion
(no early exit, context compression handled automatically). Processes IDs in
configurable batches with snapshot-based incremental fetch
(snapshot_fetch.py) for resume and --reprocess support, then emits a run
report and counts summary.

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
