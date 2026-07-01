---
title: docs-review-technical
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-review-technical

Multi-agent technical accuracy review with optional code-aware validation.
Shares the discovery/changed-range/confidence pipeline with
`docs-review-style` but focuses on correctness: an Opus `technical-reviewer`
agent checks commands, APIs, configs, and claims, and a conditional
code-aware agent clones the source repo (from `--code`, the PR, a `--jira`
ticket, or `:code-repo-url:` attributes), reuses any `learn-code` analysis,
and classifies each claim as verified / inaccurate / stale / unverifiable.
Results run through a 5-pass evidence-based triage, per-issue validation, a
whole-repo anti-pattern/blast-radius scan, and confidence + changed-range
filtering. Supports `--local`/`--pr` (+`--post-comments`) and `--fix`.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-review-technical diagram](docs-review-technical.svg)
</div>

## Arguments

```bash
/docs-review-technical [--local | --pr <url> [--post-comments]] [--code <url>]... [--jira <ticket>] [--ref <branch>] [--fix] [--threshold <0-100>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--local` |  | - | Review documentation changes in the current branch vs the base branch. |
| `--pr` |  | - | Review documentation changes in a GitHub PR or GitLab MR. |
| `--post-comments` |  | `false` | Post findings as inline PR/MR comments (with --pr). |
| `--code` |  | - | Source repo URL for code-aware validation (enables the code-aware agent). Repeatable. |
| `--jira` |  | - | Auto-discover code repos linked from a JIRA ticket. |
| `--ref` |  | - | Git ref to check out in the preceding --code repo. |
| `--fix` |  | `false` | Auto-fix issues at >=65% confidence, then walk through the rest interactively. |
| `--threshold` |  | `80` | Confidence threshold for reporting issues. |

## Usage

```bash
/docs-review-technical --local --code https://github.com/org/repo
/docs-review-technical --pr https://github.com/org/repo/pull/42 --post-comments
/docs-review-technical --local --jira PROJ-123 --fix
```
