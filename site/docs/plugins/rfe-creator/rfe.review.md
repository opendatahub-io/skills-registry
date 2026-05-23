---
title: rfe.review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.review

Score and improve RFEs with a multi-phase agent pipeline. Accepts one or
more Jira keys (RHAIRFE-NNNN) or local IDs (RFE-NNN). Fetches missing
RFEs from Jira, runs rubric-based assessment via assess-rfe, launches
parallel feasibility checks, synthesizes review files with scored
criteria, auto-revises failing RFEs, and re-assesses (up to 2 cycles).
The orchestrator never reads RFE content directly -- all content-heavy
work is delegated to sub-agents (fetch, assess, feasibility, review,
revise).

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.review diagram](rfe.review.svg)
</div>

## Arguments

```bash
/rfe.review <ID> [ID2 ...] [--headless] [--caller <name>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ID` | :material-check: | - | One or more space-separated RFE IDs (RHAIRFE-NNNN or RFE-NNN) |
| `--headless` |  | - | Suppress end-of-run summary; used when called from rfe.auto-fix or rfe.split |
| `--caller` |  | `none` | Identifies calling skill for headless return routing |

## Usage

```bash
/rfe.review RHAIRFE-1234
/rfe.review RFE-001 RFE-002 RFE-003
/rfe.review --headless --caller autofix RHAIRFE-1234 RHAIRFE-5678
```
