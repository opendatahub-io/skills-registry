---
title: testability-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# testability-review

Internal forked reviewer sub-agent for strat.review. Determines whether
strategy acceptance criteria are testable and measurable, identifies
missing edge cases (failure modes, boundary conditions, concurrent
access, large-scale scenarios), assesses test complexity, and evaluates
whether non-functional requirements (performance, security, scalability)
can be validated with concrete tests. Suggests specific rewrites for
vague criteria.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![testability-review diagram](testability-review.svg)
</div>

## Usage

```bash
/testability-review
```
