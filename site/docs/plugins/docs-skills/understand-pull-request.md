---
title: understand-pull-request
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# understand-pull-request

Analyzes a pull request or merge request and produces a structured
PR-ANALYSIS.md. It fetches PR/MR metadata and the diff via `git-pr-reader`,
builds a brief repo overview (reusing a prior `learn-code` ONBOARDING.md if
present, otherwise dispatching a `pr-repo-summarizer` agent), identifies the
affected modules, then fans out `pr-change-analyzer` agents (in batches of 10)
— each analyzing one module's diff hunks in context — and a
`pr-synthesis-writer` agent assembles the final document. Auto-detects
GitHub/GitLab from the URL or git remote; progress is checkpointed for resume.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![understand-pull-request diagram](understand-pull-request.svg)
</div>

## Arguments

```bash
/understand-pull-request <pr-number-or-url> [--repo <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `pr` | :material-check: | - | PR/MR number or full GitHub/GitLab URL. |
| `--repo` |  | - | Local repository checkout path (defaults to the current directory). |

## Usage

```bash
/understand-pull-request 42
/understand-pull-request 42 --repo /path/to/repo
/understand-pull-request https://github.com/org/repo/pull/42
```
