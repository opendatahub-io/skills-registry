---
title: odh-git
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-git

Git utilities, GitHub/GitLab workflow automation, and CI debugging

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">git</span> <span class="tag-pill">github</span> <span class="tag-pill">gitlab</span> <span class="tag-pill">ci</span> <span class="tag-pill">gist</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/aipcc-commit-suggest`](aipcc-commit-suggest.md) | Generate AIPCC Commits style commit messages or summarize existing commits | :material-check: |
| [`/gist-upload`](gist-upload.md) | Use this skill to upload a summary or plan from the current conversation as a GitHub Gist using the `gh` CLI. | :material-check: |
| [`/git-shallow-clone`](git-shallow-clone.md) | Use this skill to perform a shallow clone of a Git repository to a temporary location. | :material-check: |
| [`/github-actions-debugger`](github-actions-debugger.md) | Debug and monitor GitHub Actions workflow runs. Check run status, view failed job logs, and troubleshoot CI failures. Use this when the user needs to investigate GitHub Actions failures, inspect job output, or identify the root cause of a broken workflow run. | :material-check: |
| [`/github-sync-upstream`](github-sync-upstream.md) | Sync code from an upstream GitHub repository into a target fork (e.g., opendatahub-io midstream). Detects remotes from the current repo, or clones fresh if run from outside. Fetches upstream, merges into a sync branch, restores protected files, resolves conflicts, and opens a PR to the target GitHub repo. Use when asked to sync upstream, merge upstream changes, or bring a GitHub fork up to date with its upstream source. | :material-check: |
| [`/gitlab-pipeline-debugger`](gitlab-pipeline-debugger.md) | Debug and monitor GitLab CI/CD pipelines for merge requests. Check pipeline status, view job logs, and troubleshoot CI failures. Use this when the user needs to investigate GitLab CI pipeline issues, check job statuses, or view specific job logs. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-git@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-git` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
