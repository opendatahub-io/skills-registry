---
title: vllm-backport-cherry-pick
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-backport-cherry-pick

Attempt automatic cherry-pick of clean backport candidates to a
downstream release branch. Selects eligible PRs (ai-fixable, score >= 50,
not already backported, verdict is must_backport or likely_relevant),
cherry-picks each, and creates a draft PR if any succeed. Requires agent
follow-up for semantic validation of the cherry-picked diff.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-backport-cherry-pick diagram](vllm-backport-cherry-pick.svg)
</div>

## Arguments

```bash
/vllm-backport-cherry-pick [--input] [--downstream] [--branch] [--jira-url] [--report-url] [--output]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | :material-check: | - | Path to ranked.json from score-rank step |
| `--downstream` | :material-check: | - | Path to downstream repository |
| `--branch` | :material-check: | - | Downstream branch name (e.g., rhai/0.13.0) |
| `--jira-url` |  | - | Jira ticket URL to link in the PR |
| `--report-url` |  | - | GitHub report URL to link in the PR |
| `--output` | :material-check: | - | Output path for cherry-pick-result.json |

## Usage

```bash
/vllm-backport-cherry-pick --input artifacts/ranked.json --downstream /path/to/repo --branch rhai/0.13.0 --output artifacts/cherry-pick-result.json
```
