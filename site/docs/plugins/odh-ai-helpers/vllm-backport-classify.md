---
title: vllm-backport-classify
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-backport-classify

Classify bugfix PRs by type (runtime_bug, platform_specific, unclear,
not_bugfix) and filter by file existence at a release tag. Applies
deterministic regex rules, checks which files existed at the target tag,
detects subsystems, and filters PRs touching only post-release or
non-runtime code. PRs classified as "unclear" require agent review.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-backport-classify diagram](vllm-backport-classify.svg)
</div>

## Arguments

```bash
/vllm-backport-classify [--input] [--repo] [--tag] [--output]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | :material-check: | - | Path to raw-prs.json from fetch-prs step |
| `--repo` | :material-check: | - | Path to local vllm repository clone |
| `--tag` | :material-check: | - | Release tag to check file existence against (e.g., v0.13.0) |
| `--output` | :material-check: | - | Output path for filtered.json |

## Usage

```bash
/vllm-backport-classify --input artifacts/raw-prs.json --repo /path/to/vllm --tag v0.13.0 --output artifacts/filtered.json
```
