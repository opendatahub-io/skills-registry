---
title: risk-assessment
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# risk-assessment

Multi-agent PR risk assessment orchestrator that coordinates four parallel
analyzer sub-agents to evaluate a GitHub pull request across complementary
dimensions: security risk and breaking changes, test coverage validation,
architecture impact and blast radius, and cross-repository intelligence
for affected test repos.

The orchestrator extracts PR metadata via gh CLI, loads context from
architecture docs and Jira, launches all four analyzers in parallel using
the Agent tool, then aggregates results through a decision engine. This is
an advisory-only system -- it provides recommendations but never blocks PRs.

Supports headless mode for CI integration and dry-run mode for testing
without publishing. Results are published as PR comments and status checks
on GitHub.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![risk-assessment diagram](risk-assessment.svg)
</div>

## Arguments

```bash
/risk-assessment <PR_NUMBER> <REPO> [--headless] [--dry-run]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PR_NUMBER` | :material-check: | - | GitHub pull request number to analyze |
| `REPO` | :material-check: | - | Repository identifier (owner/repo format) |
| `--headless` |  | - | Run in headless mode for CI integration |
| `--dry-run` |  | - | Run analysis without publishing results to GitHub |

## Usage

```bash
/risk-assessment 123 opendatahub-io/odh-dashboard
/risk-assessment 456 opendatahub-io/kserve --dry-run
```
