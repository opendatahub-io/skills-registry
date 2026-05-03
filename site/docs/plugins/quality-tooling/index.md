<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# quality-tooling

Quality tooling and automation for RHOAI component development. Includes automated repository analysis, build validation, and test pattern extraction.

!!! info "Plugin Details"

    - **Version**: 1.0.0
    - **Author**: Anthony Coughlin
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [antowaddle/Red-Hat-Quality-Tiger-Team](https://github.com/antowaddle/Red-Hat-Quality-Tiger-Team)
    - **Tags**: quality, testing, ci-cd, build-validation, analysis

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

## Installation

```bash
/plugin install quality-tooling@opendatahub-skills
```
