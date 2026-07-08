---
title: strat-creator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strat-creator

Claude Code skills for creating, reviewing, and submitting strategies to the RHAISTRAT Jira project. Provides an automated pipeline from initial creation through refinement, adversarial review with independent reviewers, and human sign-off workflow with pull/push/signoff gates.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: Eder Ignatowicz
    - **Category**: [Product Planning](../../categories/planning.md)
    - **Repository**: [opendatahub-io/strat-creator](https://github.com/opendatahub-io/strat-creator)
    - **Tags**: <span class="tag-pill">strategy</span> <span class="tag-pill">strat</span> <span class="tag-pill">jira</span> <span class="tag-pill">review</span> <span class="tag-pill">pipeline</span>

## Dependencies

- [`assess-strat`](../assess-strat/index.md)

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/strategy-create`](strategy-create.md) | Create strategies from approved RFEs by cloning them to RHAISTRAT in Jira | :material-check: |
| [`/strategy-refine`](strategy-refine.md) | Refine a strategy with technical HOW, dependencies, and NFRs | :material-check: |
| [`/strategy-review`](strategy-review.md) | Adversarial review with rubric scoring and independent forked reviewers | :material-check: |
| [`/strategy-pull`](strategy-pull.md) | Pull a post-CI strategy from Jira into local workspace for human review | :material-check: |
| [`/strategy-push`](strategy-push.md) | Push a locally-refined strategy back to Jira and resubmit to CI | :material-check: |
| [`/strategy-signoff`](strategy-signoff.md) | Sign off on a CI-approved strategy with human sign-off label | :material-check: |
| [`/export-rubric`](export-rubric.md) | Export the scoring rubric to artifacts/strat-rubric.md | :material-check: |
| [`/strategy-feasibility-review`](strategy-feasibility-review.md) | Reviews strategy for technical feasibility and effort estimate credibility | :material-close: internal |
| [`/strategy-testability-review`](strategy-testability-review.md) | Reviews strategy for testability and measurable acceptance criteria | :material-close: internal |
| [`/strategy-scope-review`](strategy-scope-review.md) | Reviews strategy for right-sizing and bounded scope | :material-close: internal |
| [`/strategy-architecture-review`](strategy-architecture-review.md) | Reviews strategy for architectural correctness and integration patterns | :material-close: internal |

## Installation

```bash
/plugin install strat-creator@opendatahub-skills
```
