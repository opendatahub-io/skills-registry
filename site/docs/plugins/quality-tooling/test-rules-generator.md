---
title: test-rules-generator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-rules-generator

Analyzes existing test patterns in a repository and generates Claude Code
agent rules in .claude/rules/ for consistent test creation. Covers unit,
mock, E2E, and contract test types with framework-specific awareness
(Jest, Cypress, Go testing, React Testing Library, pytest).

The generation process has three phases: repository analysis (identify test
directories, frameworks, and test types), pattern extraction (sample 5-10
representative files per type, extract structure, naming, setup/teardown,
assertion styles), and rule generation (produce markdown files with
description, structure, examples, conventions, and checklists). The output
serves as living documentation that enables agents to auto-create tests
following established repository conventions.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-rules-generator diagram](test-rules-generator.svg)
</div>

## Arguments

```bash
/test-rules-generator [repository-url]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository-url` |  | - | GitHub repository URL to extract test patterns from (prompted if omitted) |

## Usage

```bash
/test-rules-generator https://github.com/opendatahub-io/odh-dashboard
/test-rules-generator https://github.com/opendatahub-io/kserve
/test-rules-generator https://github.com/kubeflow/training-operator
```
