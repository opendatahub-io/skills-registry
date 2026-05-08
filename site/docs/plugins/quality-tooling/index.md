---
title: quality-tooling
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# quality-tooling

Quality tooling and automation suite for RHOAI component development. Provides
five complementary skills that span the full quality lifecycle: repository-wide
quality assessment against gold standards, Konflux build simulation for catching
failures at PR time, test pattern extraction for generating agent rules,
historical bug coverage analysis with Jira integration, and multi-dimensional
PR risk assessment with parallel analyzer agents.

The plugin targets Red Hat OpenShift AI repositories and understands RHOAI-specific
concerns such as FIPS compliance, hermetic builds, module federation, operator
packaging, and cross-repo test dependencies. All skills produce rich output
artifacts -- interactive HTML reports, GitHub Actions workflows, or markdown
rule files -- that are immediately actionable without manual post-processing.


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

## Architecture

Each skill operates independently as a standalone analysis pipeline invoked via
slash command. The common pattern is: clone or access a target repository, perform
deep structural analysis, and generate output artifacts (HTML reports, YAML configs,
GitHub Actions workflows, or markdown rule files).

The risk-assessment skill is the most architecturally complex: it uses an
orchestrator pattern that launches four parallel sub-agents (risk analyzer, test
validator, impact analyzer, cross-repo analyzer) via the Agent tool, then
aggregates their results through a decision engine. Shell scripts handle PR
extraction, context loading, output verification, and result reporting.

The historical-bug-coverage skill integrates with Jira via environment-configured
credentials and uses Python modules for deep test analysis (Jest, Cypress, pytest,
Go test), confidence scoring, and HTML report generation.

Several skills share conceptual overlap (quality-repo-analysis and test-rules-generator
both analyze test infrastructure) but operate at different abstraction levels --
scoring vs. pattern extraction.
