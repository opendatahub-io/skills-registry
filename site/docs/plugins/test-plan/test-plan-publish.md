---
title: test-plan-publish
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-publish

Publish test plan artifacts to GitHub by creating a branch, committing all files,
and opening a pull request. Validates frontmatter and artifacts before publishing.
Supports updating existing PRs (pushes new commits to the same branch). Uses
version-free branch names (test-plan/<source_key>) for iterative updates.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-publish diagram](test-plan-publish.svg)
</div>

## Arguments

```bash
/test-plan-publish [FEATURE_SOURCE] [--repo owner/repo] [--reviewers user1,user2]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `FEATURE_SOURCE` |  | `auto-detected from prior /test-plan-create run` | Feature directory path, GitHub branch URL, or GitHub PR URL |
| `--repo` |  | - | Target GitHub repository in owner/repo format |
| `--reviewers` |  | - | Comma-separated list of GitHub usernames to assign as PR reviewers |

## Usage

```bash
/test-plan-publish tool_calling_metadata
/test-plan-publish tool_calling_metadata --reviewers alice,bob
/test-plan-publish tool_calling_metadata --repo org/test-plans-repo
```
