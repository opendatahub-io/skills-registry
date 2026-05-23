---
title: python-packaging-bug-finder
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-bug-finder

Find known packaging bugs, fixes, and workarounds for Python projects
by searching GitHub issues. First uses source-finder to locate the repo,
then searches issues for build, installation, dependency, compiler, and
platform-specific problems. Analyzes resolution status, version impact,
and available workarounds for each issue found.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-bug-finder diagram](python-packaging-bug-finder.svg)
</div>

## Arguments

```bash
/python-packaging-bug-finder <PACKAGE_NAME>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PACKAGE_NAME` | :material-check: | - | Python package name to search issues for |

## Usage

```bash
/python-packaging-bug-finder torch
/python-packaging-bug-finder numpy
```
