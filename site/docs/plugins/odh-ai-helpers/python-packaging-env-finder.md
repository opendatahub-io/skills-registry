---
title: python-packaging-env-finder
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-env-finder

Investigate environment variables that can be set when building Python
wheels for a given project. Analyzes setup.py, CMake files, and other
build configuration files to discover compiler variables (CC, CXX, CFLAGS),
path configuration, feature control flags (ENABLE_*, WITH_*, USE_*), and
Python-specific build variables.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-env-finder diagram](python-packaging-env-finder.svg)
</div>

## Arguments

```bash
/python-packaging-env-finder [PROJECT_PATH]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PROJECT_PATH` |  | `current directory` | Path to the Python project to analyze |

## Usage

```bash
/python-packaging-env-finder
/python-packaging-env-finder /path/to/project
```
