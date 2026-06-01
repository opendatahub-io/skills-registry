---
title: python-packaging-license-finder
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-license-finder

Deterministically find license information for Python packages using a
two-step approach: first check PyPI metadata via a helper script, then
fall back to cloning the source repository and reading LICENSE files
directly. Can also accept a source URL to skip PyPI lookup entirely.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-license-finder diagram](python-packaging-license-finder.svg)
</div>

## Arguments

```bash
/python-packaging-license-finder <PACKAGE_NAME> [VERSION] [--source-url]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PACKAGE_NAME` | :material-check: | - | Python package name |
| `VERSION` |  | `latest` | Specific package version |
| `--source-url` |  | - | Source repository URL (skips PyPI lookup) |

## Usage

```bash
/python-packaging-license-finder requests
/python-packaging-license-finder django 4.2.0
/python-packaging-license-finder some-pkg --source-url https://github.com/org/repo
```
