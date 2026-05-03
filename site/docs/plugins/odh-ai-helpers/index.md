<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-ai-helpers

Developer productivity tools for Python packaging, CI/CD debugging, and workflow automation. Includes skills for analyzing package build complexity, resolving dependencies, finding licenses, debugging GitLab pipelines, reviewing ADRs, and more.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Repository**: [opendatahub-io/ai-helpers](https://github.com/opendatahub-io/ai-helpers)
    - **Tags**: <span class="tag-pill">python-packaging</span> <span class="tag-pill">licensing</span> <span class="tag-pill">dependencies</span> <span class="tag-pill">gitlab</span> <span class="tag-pill">jira</span> <span class="tag-pill">adr</span> <span class="tag-pill">git</span> <span class="tag-pill">automation</span>

## Pipeline

<div class="diagram-container" markdown>
![odh-ai-helpers pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/adr-review`](adr-review.md) | Review an Architectural Decision Record (ADR) using a team of specialist reviewer subagents and produce a consolidated report | :material-check: |
| [`/gitlab-pipeline-debugger`](gitlab-pipeline-debugger.md) | Debug and monitor GitLab CI/CD pipelines for merge requests, check pipeline status, view job logs, and troubleshoot CI failures | :material-check: |
| [`/git-shallow-clone`](git-shallow-clone.md) | Perform a shallow clone of a Git repository to a temporary location | :material-check: |
| [`/jira-upload-chat-log`](jira-upload-chat-log.md) | Export and upload the current chat conversation as a markdown file attachment to a Jira ticket | :material-check: |
| [`/python-full-deps`](python-full-deps.md) | Resolve the full install-time dependency tree for a Python package with environment markers | :material-check: |
| [`/python-packaging-bug-finder`](python-packaging-bug-finder.md) | Find known packaging bugs, fixes, and workarounds for Python projects by searching GitHub issues | :material-check: |
| [`/python-packaging-complexity`](python-packaging-complexity.md) | Analyze Python package build complexity by inspecting PyPI metadata, compilation requirements, and distribution types | :material-check: |
| [`/python-packaging-env-finder`](python-packaging-env-finder.md) | Investigate environment variables that can be set when building Python wheels for a given project | :material-check: |
| [`/python-packaging-license-checker`](python-packaging-license-checker.md) | Check whether a Python package license is compatible with redistribution in Red Hat products | :material-check: |
| [`/python-packaging-license-finder`](python-packaging-license-finder.md) | Deterministically find license information for Python packages by checking PyPI metadata and Git repository LICENSE files | :material-check: |
| [`/python-packaging-source-finder`](python-packaging-source-finder.md) | Locate source code repositories for Python packages by analyzing PyPI metadata and project URLs | :material-check: |

## Agents

| Agent | Description |
|-------|-------------|
| python-packaging-investigator | Investigates Python package repositories to analyze build systems, dependencies, and packaging complexity |

## Installation

```bash
/plugin install odh-ai-helpers@opendatahub-skills
```
