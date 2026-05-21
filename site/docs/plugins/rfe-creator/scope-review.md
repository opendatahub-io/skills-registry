---
title: scope-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# scope-review

Internal forked reviewer sub-agent for strat.review. Assesses whether
each strategy is right-sized -- not too big (needs splitting), not too
small (just a task), and scoped to match its effort estimate. Checks
that scope is clearly bounded, deliverables are complete capabilities,
and flags scope traps like "and related functionality" or "full support
for". Verifies the strategy neither silently expands nor shrinks the
original RFE scope.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![scope-review diagram](scope-review.svg)
</div>

## Usage

```bash
/scope-review
```
