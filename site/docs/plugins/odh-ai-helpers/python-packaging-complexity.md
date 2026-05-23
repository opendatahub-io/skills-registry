---
title: python-packaging-complexity
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-complexity

Analyze Python package build complexity by inspecting PyPI metadata.
Evaluates compilation requirements (C/C++/Rust/Fortran), dependency
complexity, distribution types (sdist, platform-specific wheels, universal
wheels), and produces a numerical complexity score (0-10+). Provides
actionable recommendations for wheel building strategies.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-complexity diagram](python-packaging-complexity.svg)
</div>

## Arguments

```bash
/python-packaging-complexity <PACKAGE_NAME> [VERSION] [--json]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PACKAGE_NAME` | :material-check: | - | Python package name to analyze |
| `VERSION` |  | `latest` | Specific package version |
| `--json` |  | - | Output as structured JSON for programmatic processing |

## Usage

```bash
/python-packaging-complexity torch
/python-packaging-complexity numpy 1.24.3
/python-packaging-complexity tensorflow --json
```
