---
title: rfe.review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.review

Score and improve RFEs with rubric-based assessment, feasibility check,
and auto-revision loop.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.review diagram](rfe.review.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--headless` |  | — | Suppress end-of-run summary |
| `--caller` |  | `none` | Identifies calling skill for headless return |

## Usage

```
/rfe.review RHAIRFE-1234
/rfe.review --headless RFE-001 RFE-002
```
