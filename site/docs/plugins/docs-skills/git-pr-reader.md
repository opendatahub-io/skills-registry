---
title: git-pr-reader
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# git-pr-reader

A unified command-line interface for GitHub Pull Requests and GitLab Merge
Requests, auto-detecting the platform from the URL. It reads PR/MR data and
diffs (with smart file filtering via YAML patterns), lists changed files,
fetches review comments (filtering bots and resolved threads), posts inline
review comments (with duplicate detection and PR-level fallback), replies to
existing comment threads, extracts and validates deterministic line numbers
from diffs, returns combined metadata, and auto-detects the open PR/MR for the
current branch. It is the shared platform layer used by `docs-review-style`,
`docs-review-technical`, `action-comments`, and the pipeline. PEP 723 script
(PyGithub / python-gitlab); auth via `GITHUB_TOKEN` / `GITLAB_TOKEN`.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![git-pr-reader diagram](git-pr-reader.svg)
</div>

## Arguments

```bash
/git-pr-reader <subcommand> <url> [options]   (read | info | files | comments | diff | post | reply | extract | metadata | detect)
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `read / info / files / comments / diff / metadata` |  | - | Read PR/MR data, info, changed files, comments, diff, or combined metadata for a URL. |
| `post / reply` |  | - | Post inline review comments from a JSON file, or reply to an existing comment thread (--comment-id / --discussion-id). |
| `extract` |  | - | Extract or validate diff line numbers (--dump, --validate) for accurate comment placement. |
| `detect` |  | - | Auto-detect the open PR/MR for the current git branch. |

## Usage

```bash
git_pr_reader.py files https://github.com/owner/repo/pull/123 --filter '*.adoc' --json
git_pr_reader.py comments https://github.com/owner/repo/pull/123 --json
git_pr_reader.py post https://github.com/owner/repo/pull/123 comments.json --review-type style
```
