---
title: eval-analyze
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-analyze

Deep-reads a target skill and generates eval.yaml -- the configuration that
/eval-run needs. Examines the skill's SKILL.md, follows sub-skill chains
recursively (up to 5 levels), explores scripts and test cases, and produces
a complete config with execution mode, dataset schema, output descriptions,
judges, model defaults, and thresholds. Uses an Explore sub-agent for the
recursive skill analysis and caches the result in eval.md with a content
hash for staleness detection.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-analyze diagram](eval-analyze.svg)
</div>

## Arguments

```bash
/eval-analyze [--skill <name>] [--config <path>] [--update]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--skill` |  | `auto-detect` | Which skill to analyze. If omitted, lists all project skills and picks automatically if only one is found. |
| `--config` |  | `eval.yaml` | Output path for the eval config file. |
| `--update` |  | `false` | Fill in missing sections only, preserving user edits. Useful for upgrading older configs. |

## Usage

```bash
/eval-analyze --skill my-skill
/eval-analyze --update
/eval-analyze --skill rfe.create --config eval-rfe.yaml
```
