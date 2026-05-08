---
title: eval-analyze
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-analyze

Deeply examines a target skill's SKILL.md, sub-skills, scripts, and test cases
to generate eval.yaml — the configuration that /eval-run needs.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-analyze diagram](eval-analyze.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--skill` |  | `auto-detect` | Which skill to analyze |
| `--config` |  | `eval.yaml` | Output path for the eval config |
| `--update` |  | `false` | Fill in missing sections only, preserve user edits |

## Usage

```
/eval-analyze --skill my-skill
/eval-analyze --update
```
