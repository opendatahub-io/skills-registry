---
title: test-plan-case-implement
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-case-implement

Generate executable test automation code (pytest, Go, Jest, etc.) from TC-*.md
test case specifications. Runs placement analysis to determine component repo vs
downstream E2E repo placement, loads repository conventions from odh-test-context,
generates test files in parallel via sub-agents, scores quality with a 5-criteria
rubric, and auto-revises low-scoring functions. Supports selective implementation
via --test-cases flag.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-case-implement diagram](test-plan-case-implement.svg)
</div>

## Arguments

```bash
/test-plan-case-implement <FEATURE_SOURCE> [--test-cases TC-ID,TC-ID] [--target-repo PATH]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `FEATURE_SOURCE` | :material-check: | - | Feature directory, GitHub PR URL, or GitHub branch containing test case artifacts |
| `--test-cases` |  | - | Comma-separated list of specific test case IDs to implement (e.g., TC-API-001,TC-E2E-001) |
| `--target-repo` |  | - | Override auto-detected target repository path or URL |

## Usage

```bash
/test-plan-case-implement features/notebooks/RHAISTRAT-400-notebook-spawning
/test-plan-case-implement https://github.com/org/repo/pull/7
/test-plan-case-implement features/notebooks/RHAISTRAT-400 --test-cases TC-API-001,TC-API-002
/test-plan-case-implement features/notebooks/RHAISTRAT-400 --target-repo ~/Code/opendatahub-tests
```
