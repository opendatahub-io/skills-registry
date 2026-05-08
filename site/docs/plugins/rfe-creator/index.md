---
title: rfe-creator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-creator

A comprehensive Claude Code skill suite for the full lifecycle of Requests for
Enhancement (RFEs) in the RHAIRFE Jira project. Covers creation from problem
statements, rubric-based review with auto-revision, intelligent splitting of
oversized RFEs, and submission to Jira. Also provides strategy document skills
(RHAISTRAT) for refining approved RFEs into implementation strategies with
adversarial multi-reviewer validation.

The plugin uses a shared artifact convention — all skills read from and write to
an `artifacts/` directory with YAML frontmatter for structured metadata. Jira
write operations use deterministic Python scripts rather than LLM tool-calling,
while read operations support both Atlassian MCP and REST API fallback.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: jwforres
    - **Category**: [Product Planning](../../categories/planning.md)
    - **Repository**: [jwforres/rfe-creator](https://github.com/jwforres/rfe-creator)
    - **Tags**: <span class="tag-pill">rfe</span> <span class="tag-pill">jira</span> <span class="tag-pill">review</span> <span class="tag-pill">strategy</span> <span class="tag-pill">pipeline</span>

## Architecture

Two skill families: RFE skills (rfe.*) for the requirements pipeline and
Strategy skills (strat.*) for implementation planning. A speedrun skill
orchestrates the full end-to-end flow by invoking other skills.

Review skills use a forked reviewer pattern — independent sub-agents
(feasibility, testability, scope, architecture) run in isolated contexts
and produce separate assessments. State persistence uses scripts/state.py
for long-running operations, and scripts/frontmatter.py manages YAML
frontmatter on all artifact files.

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
