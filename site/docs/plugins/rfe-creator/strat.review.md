---
title: strat.review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strat.review

Adversarial review of refined strategies. Spawns 4 independent forked
reviewers in parallel -- architecture-review, feasibility-review,
scope-review, and testability-review -- each running in isolated context.
Synthesizes findings into per-strategy review files preserving both
agreements and disagreements between reviewers. Supports re-review
after revisions.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![strat.review diagram](strat.review.svg)
</div>

## Usage

```bash
/strat.review
```
