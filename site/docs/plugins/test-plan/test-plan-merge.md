---
title: test-plan-merge
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-merge

Internal forked sub-agent for intelligent merge of new analyzer findings into
an existing test plan. Applies section-by-section merge logic (additive for scope
and endpoints, replacement for boilerplate priorities, preserving user edits).
Returns updated section content, change summary, and merge statistics.

**Plugin**: [test-plan](index.md) | **:material-close: Internal**

## Diagram

<div class="diagram-container" markdown>
![test-plan-merge diagram](test-plan-merge.svg)
</div>

## Usage

```bash
/test-plan-merge
```
