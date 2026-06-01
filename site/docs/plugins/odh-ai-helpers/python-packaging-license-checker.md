---
title: python-packaging-license-checker
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-license-checker

Check whether a Python package license is compatible with redistribution
in Red Hat products, using the Fedora License Data as the authoritative
policy source. Clones the source repo to read the actual LICENSE file
(not just PyPI metadata), normalizes to SPDX identifiers, handles
compound AND/OR expressions, checks vendor agreements (NVIDIA, Intel
Gaudi, IBM Spyre), and performs build and export compliance checks.
Produces a structured six-field verdict: License, Source verified,
Verdict, Build compliance, Export compliance, and Notes.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-license-checker diagram](python-packaging-license-checker.svg)
</div>

## Arguments

```bash
/python-packaging-license-checker <PACKAGE_NAME> [--repo-url] [--source-available] [--upstream-org]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PACKAGE_NAME` | :material-check: | - | Python package name to check |
| `--repo-url` |  | - | Source repository URL (skips source-finder step) |
| `--source-available` |  | - | Whether buildable source exists |
| `--upstream-org` |  | - | Name and primary country of the maintaining organization |

## Usage

```bash
/python-packaging-license-checker requests
/python-packaging-license-checker some-package --repo-url https://github.com/org/repo
```
