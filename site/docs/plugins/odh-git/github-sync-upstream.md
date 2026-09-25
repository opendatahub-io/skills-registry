---
title: github-sync-upstream
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# github-sync-upstream

Sync code from an upstream GitHub repository into a target fork (e.g., opendatahub-io midstream). Detects remotes from the current repo, or clones fresh if run from outside. Fetches upstream, merges into a sync branch, restores protected files, resolves conflicts, and opens a PR to the target GitHub repo. Use when asked to sync upstream, merge upstream changes, or bring a GitHub fork up to date with its upstream source.

**Plugin**: [odh-git](index.md) | **:material-check: User-invocable**

## Usage

```bash
/github-sync-upstream
```
