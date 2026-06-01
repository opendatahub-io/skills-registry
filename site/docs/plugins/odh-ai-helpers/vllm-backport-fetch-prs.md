---
title: vllm-backport-fetch-prs
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-backport-fetch-prs

Fetch merged bugfix PRs from vllm-project/vllm within a configurable
date window using GitHub CLI. Uses multiple search queries (label:bug,
[Bugfix]/[BugFix]/[Bug Fix] title patterns) and deduplicates results.
Also detects reverted PRs. Outputs a JSON array of PR objects to stdout.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-backport-fetch-prs diagram](vllm-backport-fetch-prs.svg)
</div>

## Arguments

```bash
/vllm-backport-fetch-prs [DAYS_BACK]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `DAYS_BACK` |  | `7` | Number of days to look back for merged PRs |

## Usage

```bash
/vllm-backport-fetch-prs
/vllm-backport-fetch-prs 14
```
