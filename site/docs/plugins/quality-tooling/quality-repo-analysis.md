---
title: quality-repo-analysis
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# quality-repo-analysis

Comprehensive quality assessment across 7 dimensions: CI/CD, test coverage,
code quality, container image testing, security practices, agent rules, and
testing frameworks. Produces markdown report and interactive HTML visualization.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![quality-repo-analysis diagram](quality-repo-analysis.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository-url` | :material-check: | — | GitHub repository URL to analyze |

## Usage

```
/quality-repo-analysis https://github.com/opendatahub-io/kserve
/quality-repo-analysis https://github.com/kubeflow/training-operator
```
