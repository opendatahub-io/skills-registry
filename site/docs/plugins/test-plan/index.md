<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan

Generate test plans and test cases from RHOAI strategies using parallel sub-agent analysis and automated review.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: Federico Mosca
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [fege/test-plan](https://github.com/fege/test-plan)
    - **Tags**: <span class="tag-pill">test-plan</span> <span class="tag-pill">test-cases</span> <span class="tag-pill">quality</span> <span class="tag-pill">strategy</span>

## Pipeline

<div class="diagram-container" markdown>
![test-plan pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/test-plan.create`](test-plan.create.md) | Generate a test plan from a strategy | :material-check: |
| [`/test-plan.create-cases`](test-plan.create-cases.md) | Generate test case files from a test plan | :material-check: |
| [`/test-plan.analyze.endpoints`](test-plan.analyze.endpoints.md) | Extract scope and API endpoints | :material-close: internal |
| [`/test-plan.analyze.risks`](test-plan.analyze.risks.md) | Determine test levels, priorities, and risks | :material-close: internal |
| [`/test-plan.analyze.infra`](test-plan.analyze.infra.md) | Identify environment and infrastructure needs | :material-close: internal |
| [`/test-plan.review`](test-plan.review.md) | Review test plan for completeness | :material-close: internal |

## Installation

```bash
/plugin install test-plan@opendatahub-skills
```
