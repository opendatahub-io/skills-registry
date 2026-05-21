---
title: vllm-backport-check-backported
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-backport-check-backported

Check which candidate PRs have already been cherry-picked into a
downstream branch. Uses two detection methods: SHA match (via git log
--grep for cherry-pick messages) and title match (via gh pr list on
the downstream branch). Adds an already_backported boolean to each PR.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-backport-check-backported diagram](vllm-backport-check-backported.svg)
</div>

## Arguments

```bash
/vllm-backport-check-backported [--input] [--downstream] [--branch] [--output]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | :material-check: | - | Path to filtered.json from classify step |
| `--downstream` | :material-check: | - | Path to downstream repository |
| `--branch` | :material-check: | - | Downstream branch name (e.g., rhai/0.13.0) |
| `--output` | :material-check: | - | Output path for candidates.json |

## Usage

```bash
/vllm-backport-check-backported --input artifacts/filtered.json --downstream /path/to/downstream --branch rhai/0.13.0 --output artifacts/candidates.json
```
