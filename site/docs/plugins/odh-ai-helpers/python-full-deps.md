---
title: python-full-deps
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-full-deps

Resolve the full install-time dependency tree for a Python package
with environment markers, using uv or pip as resolver.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-full-deps diagram](python-full-deps.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `package_name` | :material-check: | — | PyPI project name (e.g., vllm) |
| `version` |  | `latest` | Specific package version |
| `python_version` |  | `3.12` | Python version for resolution |

## Usage

```
/python-full-deps requests
/python-full-deps requests 2.32.3 3.11
```
