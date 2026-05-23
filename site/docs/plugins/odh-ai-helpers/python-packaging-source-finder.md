---
title: python-packaging-source-finder
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-source-finder

Locate source code repositories for Python packages by analyzing PyPI
metadata, project URLs, and code hosting platforms (GitHub, GitLab,
Bitbucket). Returns a JSON result with repository URL, confidence level
(high/medium/low), and the method used to find it. Falls back to web
search when PyPI metadata is insufficient.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-source-finder diagram](python-packaging-source-finder.svg)
</div>

## Arguments

```bash
/python-packaging-source-finder <PACKAGE_NAME>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PACKAGE_NAME` | :material-check: | - | Python package name to find the repository for |

## Usage

```bash
/python-packaging-source-finder requests
/python-packaging-source-finder vllm
```
