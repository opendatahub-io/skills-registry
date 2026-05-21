---
title: architecture-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# architecture-review

Internal forked reviewer sub-agent for strat.review. Checks strategy
features for architectural correctness -- verifies dependencies against
architecture docs, validates integration patterns match actual component
communication, checks component boundaries are respected, verifies
deployment model correctness, identifies architectural conflicts, and
flags cross-component coordination needs. Requires architecture context;
skips if unavailable. Runs with model: opus.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![architecture-review diagram](architecture-review.svg)
</div>

## Usage

```bash
/architecture-review
```
