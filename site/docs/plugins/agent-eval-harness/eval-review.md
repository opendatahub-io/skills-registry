---
title: eval-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-review

Interactive human-in-the-loop review of evaluation results. Presents judge
scores and skill outputs case by case, collects qualitative feedback, delegates
transcript analysis to Explore sub-agents to identify inefficiencies (roundabout
paths, multiple approaches, unnecessary tools), identifies judge-human alignment
gaps, and proposes targeted SKILL.md improvements grounded in feedback evidence.
Complements /eval-optimize (automated) by catching tone, intent, and UX issues
that judges cannot measure.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-review diagram](eval-review.svg)
</div>

## Arguments

```bash
/eval-review --run-id <id> [--config <path>] [--case <filter>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--run-id` | :material-check: | - | Which eval run to review. |
| `--config` |  | `eval.yaml` | Path to eval config. |
| `--case` |  | - | Substring match to select specific cases for review. |

## Usage

```bash
/eval-review --run-id 2026-05-01-opus
/eval-review --run-id 2026-05-01-opus --case case-003
```
