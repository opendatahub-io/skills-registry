<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan.create-cases

Generate individual test case files (TC-*.md) from an existing test plan.
Supports upgrade-aware cases and validates endpoint coverage.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan.create-cases diagram](test-plan.create-cases.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `FEATURE_DIR` |  | `auto-detected from prior /test-plan.create` | Feature directory, GitHub branch URL, or PR URL |
| `--output-dir` |  | — | Force creation in specified directory |

## Usage

```
/test-plan.create-cases
/test-plan.create-cases mcp_catalog
/test-plan.create-cases /path/to/feature_dir
```
