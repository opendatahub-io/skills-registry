---
title: python-packaging-complexity
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-complexity

Analyze Python package build complexity by inspecting PyPI metadata,
compilation requirements, and distribution types.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-complexity diagram](python-packaging-complexity.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `package_name` | :material-check: | — | Python package name to analyze |
| `version` |  | `latest` | Specific package version |
| `--json` |  | — | Output as structured JSON |

## Usage

```
/python-packaging-complexity torch
/python-packaging-complexity numpy 1.24.3 --json
```
