---
title: rfe.split
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.split

Decompose oversized RFEs into appropriately-scoped pieces. Launches
parallel split agents that analyze the parent RFE and generate child
RFEs, then invokes rfe.review on all children. Includes a self-correction
loop (1 cycle max) that re-splits children still scoring poorly on
right-sizing. Validates coverage to ensure all original scope items
are represented in the children.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.split diagram](rfe.split.svg)
</div>

## Arguments

```bash
/rfe.split <ID> [ID2 ...] [--headless]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ID` | :material-check: | - | One or more space-separated RFE IDs (RHAIRFE-NNNN or RFE-NNN) to split |
| `--headless` |  | - | Suppress end-of-run summary; used when called from rfe.auto-fix |

## Usage

```bash
/rfe.split RHAIRFE-1234
/rfe.split RHAIRFE-1234 RHAIRFE-5678
```
