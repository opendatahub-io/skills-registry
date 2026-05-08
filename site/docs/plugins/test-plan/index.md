---
title: test-plan
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan

Generate test plans and test cases from RHOAI strategies using parallel
sub-agent analysis and automated review with a 5-criteria quality rubric.


!!! info "Plugin Details"

    - **Version**: 0.2.0
    - **Author**: Federico Mosca
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [fege/test-plan](https://github.com/fege/test-plan)
    - **Tags**: <span class="tag-pill">test-plan</span> <span class="tag-pill">test-cases</span> <span class="tag-pill">quality</span> <span class="tag-pill">strategy</span> <span class="tag-pill">review</span> <span class="tag-pill">scoring</span> <span class="tag-pill">automation</span> <span class="tag-pill">playwright</span> <span class="tag-pill">ui-testing</span>

## Pipeline

<div class="diagram-container" markdown>
![test-plan pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/test-plan.create`](test-plan.create.md) | Generate a test plan from a strategy | :material-check: |
| [`/test-plan.create-cases`](test-plan.create-cases.md) | Generate test case files from a test plan | :material-check: |
| [`/test-plan.update`](test-plan.update.md) | Update test plan with new docs (ADR, API specs), re-analyze, bump version | :material-check: |
| [`/test-plan.case-implement`](test-plan.case-implement.md) | Generate executable test automation code from TC specifications with intelligent placement | :material-check: |
| [`/test-plan.ui-verify`](test-plan.ui-verify.md) | Verify UI test cases from a PR against a live ODH/RHOAI cluster via Playwright; supports upgrade testing workflow | :material-check: |
| [`/test-plan.publish`](test-plan.publish.md) | Publish test plan artifacts to GitHub with PR creation | :material-check: |
| [`/test-plan.resolve-feedback`](test-plan.resolve-feedback.md) | Assess and resolve PR review comments on test plans | :material-check: |
| [`/test-plan.score`](test-plan.score.md) | Score test plan quality using rubric without auto-revision | :material-check: |
| [`/test-plan.analyze.endpoints`](test-plan.analyze.endpoints.md) | Extract scope and API endpoints | :material-close: internal |
| [`/test-plan.analyze.risks`](test-plan.analyze.risks.md) | Determine test levels, priorities, NFRs, and risks | :material-close: internal |
| [`/test-plan.analyze.infra`](test-plan.analyze.infra.md) | Identify environment and infrastructure needs | :material-close: internal |
| [`/test-plan.merge`](test-plan.merge.md) | Intelligently merge new analyzer findings into existing test plan | :material-close: internal |
| [`/test-plan.resolve-gaps`](test-plan.resolve-gaps.md) | Cross-reference gaps with new findings to determine what's resolved | :material-close: internal |
| [`/test-plan.analyze.placement`](test-plan.analyze.placement.md) | Analyze test cases and recommend placement (component repo vs downstream) | :material-close: internal |
| [`/test-plan.review`](test-plan.review.md) | Review test plan with 5-criteria rubric and auto-revision | :material-close: internal |
| [`/test-plan.create.test-function`](test-plan.create.test-function.md) | Generate test function code from TC specification matching repo conventions | :material-close: internal |
| [`/test-plan.score.test-function`](test-plan.score.test-function.md) | Score generated test function code using 5-criteria quality rubric | :material-close: internal |

## Installation

```bash
/plugin install test-plan@opendatahub-skills
```
