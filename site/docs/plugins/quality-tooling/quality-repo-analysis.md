---
title: quality-repo-analysis
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# quality-repo-analysis

Comprehensive quality assessment that evaluates a repository across seven
dimensions: CI/CD pipeline analysis, test coverage assessment, code quality
tools, container image testing, security practices, agent rules assessment,
and testing frameworks. Compares findings against gold standard repositories
(odh-dashboard, notebooks, kserve) and produces a weighted overall score.

Generates two output formats automatically: a markdown report with YAML
frontmatter containing structured scorecard data, and an interactive HTML
report with animated score visualizations, collapsible sections, and
color-coded severity indicators. The HTML report opens in the default
browser upon completion.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![quality-repo-analysis diagram](quality-repo-analysis.svg)
</div>

## Arguments

```bash
/quality-repo-analysis [repository-url]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository-url` |  | - | GitHub repository URL to analyze (prompted if omitted) |

## Usage

```bash
/quality-repo-analysis https://github.com/opendatahub-io/kserve
/quality-repo-analysis https://github.com/kubeflow/training-operator
```
