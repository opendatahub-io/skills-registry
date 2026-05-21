---
title: rfe-feasibility-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-feasibility-review

Internal sub-agent launched by rfe.review. Reviews individual RFEs for
technical feasibility against platform architecture. Uses three verdicts:
feasible (can be built), infeasible (platform architecture fundamentally
conflicts), indeterminate (RFE too ambiguous to assess). Distinguishes
between capabilities not yet existing (feasible) and architectural
incompatibilities (infeasible). Reads Jira comment history for additional
context. Outputs to artifacts/rfe-reviews/{ID}-feasibility.md. Runs
with model: opus.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe-feasibility-review diagram](rfe-feasibility-review.svg)
</div>

## Usage

```bash
/rfe-feasibility-review
```
