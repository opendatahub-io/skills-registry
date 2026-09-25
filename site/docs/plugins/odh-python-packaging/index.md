---
title: odh-python-packaging
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-python-packaging

Python package analysis, security auditing, and build complexity assessment

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">python-packaging</span> <span class="tag-pill">licensing</span> <span class="tag-pill">dependencies</span> <span class="tag-pill">security-audit</span>

## Dependencies

- [`odh-git`](../odh-git/index.md)

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/python-full-deps`](python-full-deps.md) | Resolve the full install-time dependency tree for a Python package. Use when the user needs all transitive dependencies, full dependency list, or install requirements resolved for a specific Python version with environment markers. | :material-check: |
| [`/python-packaging-binary-audit`](python-packaging-binary-audit.md) | Scan a Python package repository for compiled/binary files using Fromager-style detection and malcontent YARA analysis, then triage findings with deterministic rules and AI reasoning to produce a structured risk report section. | :material-check: |
| [`/python-packaging-bug-finder`](python-packaging-bug-finder.md) | Use when you need to find known packaging bugs, fixes, and workarounds for Python projects by searching GitHub issues and analyzing their resolution status | :material-check: |
| [`/python-packaging-complexity`](python-packaging-complexity.md) | Use this skill to analyze Python package build complexity by inspecting PyPI metadata. Evaluates compilation requirements, dependencies, distribution types, and provides recommendations for wheel building strategies. | :material-check: |
| [`/python-packaging-env-finder`](python-packaging-env-finder.md) | Use this skill to investigate environment variables that can be set when building Python wheels for a given project. Analyzes setup.py, CMake files, and other build configuration files to discover customizable build environment variables. | :material-check: |
| [`/python-packaging-git-audit`](python-packaging-git-audit.md) | Inspect recent git history of a Python package repository for suspicious commits touching supply-chain-sensitive files, then triage findings with AI reasoning to produce a structured risk report section. | :material-check: |
| [`/python-packaging-license-checker`](python-packaging-license-checker.md) | Use this skill to check whether a Python package license is compatible with redistribution in Red Hat products, using the Fedora License Data as the authoritative policy source. Produces a structured six-field verdict with escalation guidance for non-trivial cases. | :material-check: |
| [`/python-packaging-license-finder`](python-packaging-license-finder.md) | Use this skill to deterministically find license information for Python packages by checking PyPI metadata first, then falling back to Git repository LICENSE files using shallow cloning. | :material-check: |
| [`/python-packaging-security-audit`](python-packaging-security-audit.md) | Use this skill to evaluate the security of a Python package repository by orchestrating static analysis, binary scanning, and git history inspection sub-skills in parallel, then combining their results into a unified security report with a risk rating. | :material-check: |
| [`/python-packaging-source-finder`](python-packaging-source-finder.md) | Use this skill to locate source code repositories for Python packages by analyzing PyPI metadata, project URLs, and code hosting platforms like GitHub, GitLab, and Bitbucket. Provides deterministic results with confidence levels. | :material-check: |
| [`/python-packaging-static-audit`](python-packaging-static-audit.md) | Run hexora static analysis on a Python package repository to detect suspicious code patterns, then triage findings with deterministic rules and AI reasoning to produce a structured risk report section. | :material-check: |

## Agents

| Agent | Description |
|-------|-------------|
| python-packaging-investigator | Investigates Python package repositories to analyze build systems, dependencies, and packaging complexity. Provides comprehensive guidance on how packages can be built from source using integrated analysis skills. |

## Installation

**Claude Code**

```bash
/plugin install odh-python-packaging@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-python-packaging` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
