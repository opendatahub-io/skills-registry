---
title: eval-optimize
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-optimize

Automated improvement loop. Identifies judge failures, analyzes transcripts,
edits SKILL.md, re-runs evaluation with regression checks, and iterates.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-optimize diagram](eval-optimize.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--max-iterations` |  | `3` | Maximum optimization iterations |
| `--config` |  | `eval.yaml` | Path to eval config |
| `--model` |  | `models.skill from config` | Model for skill execution |

## Usage

```
/eval-optimize
/eval-optimize --max-iterations 5 --model claude-opus-4-6
```
