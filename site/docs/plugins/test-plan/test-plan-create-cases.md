---
title: test-plan-create-cases
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-create-cases

Generate individual test case specification files (TC-*.md) from an existing test plan.
Processes categories one at a time, generates E2E and optional upgrade test cases,
validates endpoint coverage, and updates the test plan with traceability data.
Supports regeneration mode for updating existing test cases.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-create-cases diagram](test-plan-create-cases.svg)
</div>

## Arguments

```bash
/test-plan-create-cases [FEATURE_SOURCE] [--output-dir PATH]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `FEATURE_SOURCE` |  | `auto-detected from prior /test-plan-create run` | Feature directory path, GitHub branch URL, or GitHub PR URL |
| `--output-dir` |  | - | Force creation in specified directory (contributor override) |

## Usage

```bash
/test-plan-create-cases
/test-plan-create-cases mcp_catalog
/test-plan-create-cases /path/to/feature_dir
```
