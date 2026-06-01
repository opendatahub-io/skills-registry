---
title: python-full-deps
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-full-deps

Resolve the full install-time transitive dependency tree for a Python
package, respecting environment markers for a specific Python version.
Uses uv pip compile (preferred) with fallback to pip install --dry-run
--report. Outputs a sorted, deduplicated list of name==version pairs.
Complements python-packaging-complexity which only shows direct
dependencies from metadata.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-full-deps diagram](python-full-deps.svg)
</div>

## Arguments

```bash
/python-full-deps <PACKAGE_NAME> [VERSION] [PYTHON_VERSION]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PACKAGE_NAME` | :material-check: | - | PyPI project name (e.g., vllm, requests) |
| `VERSION` |  | `latest` | Specific package version (e.g., 0.4.0) |
| `PYTHON_VERSION` |  | `3.12` | Python version for environment marker resolution (e.g., 3.11) |

## Usage

```bash
/python-full-deps requests
/python-full-deps vllm 0.4.0 3.11
```
