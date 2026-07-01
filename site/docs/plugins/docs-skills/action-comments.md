---
title: action-comments
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# action-comments

Fetches unresolved review comments from a GitHub PR or GitLab MR (via
`git-pr-reader`) and actions them on local files. Auto-detects the PR/MR for
the current branch, checks out the correct branch, categorizes each comment
(Required / Suggestion / Question / Outdated), and detects outdated comments
by checking whether the reviewer's quoted text still appears near the
referenced line. Runs interactively by default (Apply / Edit / Skip / View
context per comment) or autonomously with `--ci`, which auto-applies fixes
and posts reply comments explaining each decision. When a
`.agent_workspace/` from a prior docs-workflow run is available, it grounds
suggested fixes against code analysis, requirements, prior technical review,
scope audit, and the source repo.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![action-comments diagram](action-comments.svg)
</div>

## Arguments

```bash
/action-comments [url] [--ci] [--include-resolved]   |   <ticket> --base-path <path> [--pr <url>] [--ci]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `url` |  | - | PR/MR URL (standalone mode). Auto-detected from the current branch if omitted. |
| `ticket` |  | - | JIRA ticket ID (workflow-step mode, when --base-path is given). |
| `--base-path` |  | - | Workflow base path — reads prior-step artifacts for grounding and writes a step-result.json sidecar. |
| `--pr` |  | - | PR/MR URL in workflow-step mode (auto-detected if omitted). |
| `--ci` |  | `false` | Run autonomously: auto-apply fixes and post reply comments explaining the rationale. |
| `--include-resolved` |  | `false` | Also process resolved comment threads, not just unresolved ones. |

## Usage

```bash
/action-comments
/action-comments https://github.com/org/repo/pull/42 --ci
/action-comments PROJ-123 --base-path .agent_workspace/proj-123 --ci
```
