---
title: rfe.submit
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.submit

Push RFEs to Jira via deterministic Python scripts using the REST API
with Basic Auth. Creates new RHAIRFE tickets for new RFEs or updates
existing tickets for fetched RFEs. Applies labels automatically based
on pipeline outcomes (auto-created, auto-revised, split-original,
split-result, needs-attention, feasibility verdicts). Non-interactive --
invoking this skill is the confirmation. Requires JIRA_SERVER,
JIRA_USER, and JIRA_TOKEN environment variables.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.submit diagram](rfe.submit.svg)
</div>

## Arguments

```bash
/rfe.submit [--dry-run] [--artifacts-dir <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--dry-run` |  | - | Validate locally without writing to Jira |
| `--artifacts-dir` |  | `artifacts` | Path to the artifacts directory |

## Usage

```bash
/rfe.submit
/rfe.submit --dry-run
```
