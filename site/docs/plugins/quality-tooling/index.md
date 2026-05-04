<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# quality-tooling

Quality tooling and automation for RHOAI component development. Includes
automated repository analysis against gold standards, Konflux build simulation
for PR validation, and test pattern extraction for agent rules.


!!! info "Plugin Details"

    - **Version**: 1.0.0
    - **Author**: Anthony Coughlin
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [antowaddle/Red-Hat-Quality-Tiger-Team](https://github.com/antowaddle/Red-Hat-Quality-Tiger-Team)
    - **Tags**: <span class="tag-pill">quality</span> <span class="tag-pill">testing</span> <span class="tag-pill">ci-cd</span> <span class="tag-pill">build-validation</span> <span class="tag-pill">analysis</span>

## Pipeline

<div class="diagram-container" markdown>
![quality-tooling pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/quality-repo-analysis`](quality-repo-analysis.md) | Automated analysis tool that evaluates CI/CD, testing, security, and best practices against gold standards | :material-check: |
| [`/konflux-build-simulator`](konflux-build-simulator.md) | Generate GitHub Actions workflows that simulate Konflux builds at PR time to catch failures before merge | :material-check: |
| [`/test-rules-generator`](test-rules-generator.md) | Extract test patterns from existing tests and generate .claude/rules/ documentation for consistency | :material-check: |
| [`/historical-bug-coverage`](historical-bug-coverage.md) | Analyzes historical blocking and critical bugs from Jira, determines what test coverage exists today with deep test inspection and confidence scoring, and generates standalone HTML reports | :material-check: |
| [`/risk-assessment`](risk-assessment.md) | Analyze PR for risk, test coverage, architecture impact, and cross-repo intelligence | :material-check: |

## Installation

```bash
/plugin install quality-tooling@opendatahub-skills
```
