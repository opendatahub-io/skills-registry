---
title: feasibility-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# feasibility-review

Internal forked reviewer sub-agent for strat.review. Assesses technical
feasibility of refined strategies -- whether the proposed approach works,
whether it delivers what the RFE asks for, whether effort estimates are
credible, and identifies hidden dependencies or integration challenges.
Adversarial stance: flags things that are harder than they look and
optimistic estimates. Runs with model: opus.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![feasibility-review diagram](feasibility-review.svg)
</div>

## Usage

```bash
/feasibility-review
```
