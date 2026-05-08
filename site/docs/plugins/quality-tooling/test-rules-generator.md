---
title: test-rules-generator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-rules-generator

Analyzes existing test patterns in a repository and generates Claude Code
agent rules (.claude/rules/) for consistent test creation across unit,
mock, E2E, and contract tests.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-rules-generator diagram](test-rules-generator.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository-url` | :material-check: | — | GitHub repository URL to analyze test patterns from |

## Usage

```
/test-rules-generator https://github.com/opendatahub-io/odh-dashboard
/test-rules-generator https://github.com/kubeflow/training-operator
```
