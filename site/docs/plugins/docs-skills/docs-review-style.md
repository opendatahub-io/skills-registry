---
title: docs-review-style
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-review-style

Multi-agent style-guide and modular-docs review with confidence scoring.
Discovers changed documentation files (local branch vs base, or a PR/MR),
extracts the exact changed line ranges so only new content is flagged, then
runs three parallel `docs-reviewer` agents (IBM style batch A, IBM/RH style
batch B, and modular-docs + content-quality). Findings are validated by
per-issue subagents, filtered by a confidence threshold (default 80) and by
changed-range scope, and reported. Supports `--local`, `--pr` (with optional
`--post-comments` for inline GitHub/GitLab comments), a fully interactive
mode, and `--fix` (auto-fix high-confidence issues, then walk through the
rest). For technical accuracy, use `docs-review-technical`.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-review-style diagram](docs-review-style.svg)
</div>

## Arguments

```bash
/docs-review-style [--local | --pr <url> [--post-comments]] [--fix] [--threshold <0-100>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--local` |  | - | Review documentation changes in the current branch vs the base branch. |
| `--pr` |  | - | Review documentation changes in a GitHub PR or GitLab MR. |
| `--post-comments` |  | `false` | Post findings as inline PR/MR comments (with --pr). |
| `--fix` |  | `false` | Auto-fix issues at >=65% confidence, then walk through the rest interactively. |
| `--threshold` |  | `80` | Confidence threshold for reporting issues. |

## Usage

```bash
/docs-review-style --local
/docs-review-style --pr https://github.com/org/repo/pull/42 --post-comments
/docs-review-style --local --fix --threshold 70
```
