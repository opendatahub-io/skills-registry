---
title: vllm-backport-score-rank
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-backport-score-rank

Score and rank backport candidates using a deterministic composite
formula (max 100 points) based on verdict (0-30), severity (5-25),
affected scope (3-20), backport risk (0-15), and self-containedness
(0-10). Filters out SKIP/already_backported PRs and assigns
backport_ease labels (ai-fixable if self-contained and safe/moderate risk).

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-backport-score-rank diagram](vllm-backport-score-rank.svg)
</div>

## Arguments

```bash
/vllm-backport-score-rank [--input] [--output]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | :material-check: | - | Path to analyzed.json with agent-added semantic fields |
| `--output` | :material-check: | - | Output path for ranked.json |

## Usage

```bash
/vllm-backport-score-rank --input artifacts/analyzed.json --output artifacts/ranked.json
```
