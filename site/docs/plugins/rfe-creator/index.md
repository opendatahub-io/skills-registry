<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-creator

Claude Code skills for creating, reviewing, and submitting RFEs to the RHAIRFE Jira project. Provides an automated pipeline from initial creation through review, splitting, and submission, plus strategy refinement skills.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: jwforres
    - **Category**: [Product Planning](../../categories/planning.md)
    - **Repository**: [jwforres/rfe-creator](https://github.com/jwforres/rfe-creator)
    - **Tags**: <span class="tag-pill">rfe</span> <span class="tag-pill">jira</span> <span class="tag-pill">review</span> <span class="tag-pill">strategy</span> <span class="tag-pill">pipeline</span>

## Pipeline

<div class="diagram-container" markdown>
![rfe-creator pipeline](pipeline.svg)
</div>

## Dependencies

- [`assess-rfe`](../assess-rfe/index.md)

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/rfe.create`](rfe.create.md) | Generate new RFEs from problem statements | :material-check: |
| [`/rfe.review`](rfe.review.md) | Score and improve RFEs with auto-revision | :material-check: |
| [`/rfe.split`](rfe.split.md) | Decompose oversized RFEs into appropriately-scoped pieces | :material-check: |
| [`/rfe.submit`](rfe.submit.md) | Push RFEs to Jira | :material-check: |
| [`/rfe.speedrun`](rfe.speedrun.md) | Execute the full RFE pipeline end-to-end | :material-check: |
| [`/rfe.auto-fix`](rfe.auto-fix.md) | Batch review, revise, and split operations | :material-check: |
| [`/strat.create`](strat.create.md) | Create strategy documents | :material-check: |
| [`/strat.refine`](strat.refine.md) | Refine strategy documents | :material-check: |
| [`/strat.review`](strat.review.md) | Review strategy documents | :material-check: |
| [`/strat.prioritize`](strat.prioritize.md) | Prioritize strategy items | :material-check: |
| [`/rfe-creator.update-deps`](rfe-creator.update-deps.md) | Update vendored dependencies | :material-check: |
| [`/architecture-review`](architecture-review.md) | Architecture review skill | :material-check: |
| [`/feasibility-review`](feasibility-review.md) | Feasibility review skill | :material-check: |
| [`/rfe-feasibility-review`](rfe-feasibility-review.md) | RFE feasibility review | :material-check: |
| [`/scope-review`](scope-review.md) | Scope review skill | :material-check: |
| [`/testability-review`](testability-review.md) | Testability review skill | :material-check: |

## Installation

```bash
/plugin install rfe-creator@opendatahub-skills
```
