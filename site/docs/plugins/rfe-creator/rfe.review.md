---
title: rfe.review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.review

Score and improve RFEs with a multi-phase agent pipeline. Accepts one or
more Jira keys (RHAIRFE-NNNN) or local IDs (RFE-NNN); missing RFEs are
fetched from Jira first. The orchestrator never reads RFE content directly
-- all content-heavy work is delegated to background sub-agents (fetch,
assess, feasibility, review, revise) launched in parallel waves and polled
via scripts/check_review_progress.py. It runs rubric-based assessment
(assess-rfe / rfe-scorer subagent), launches per-RFE feasibility checks
(rfe-feasibility-review), synthesizes scored review files, auto-revises
failing RFEs (filter_for_revision.py), and re-assesses up to 2 cycles,
preserving cumulative scores and revision history across cycles. Can return
headlessly to a calling skill (auto-fix or split) or print an interactive
summary with next-step suggestions.

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
