---
title: test-plan-resolve-gaps
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-resolve-gaps

Internal forked sub-agent that cross-references existing test plan gaps with
new analyzer findings and documentation. Uses semantic matching to determine
which gaps are resolved, which remain open, and identifies new gaps. Returns
structured output with resolved/unresolved/new gaps and statistics.

**Plugin**: [test-plan](index.md) | **:material-close: Internal**

## Diagram

<div class="diagram-container" markdown>
![test-plan-resolve-gaps diagram](test-plan-resolve-gaps.svg)
</div>

## Usage

```bash
/test-plan-resolve-gaps
```
