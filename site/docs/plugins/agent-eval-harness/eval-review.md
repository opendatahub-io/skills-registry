---
title: eval-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-review

Interactive human-in-the-loop review of evaluation results. Loads
summary.yaml and any /eval-run analysis.md, presents judge scores and skill
outputs case by case, collects qualitative feedback, and delegates transcript
analysis to Explore sub-agents to identify inefficiencies (roundabout paths,
multiple approaches, unnecessary tools, wasted turns). Identifies
judge-human alignment gaps and suggests new judge candidates, persists
feedback to review.yaml (keyed by case directory name for /eval-optimize and
/eval-mlflow to consume), and proposes targeted SKILL.md edits as before/after
diffs grounded in feedback evidence -- applied only with explicit approval.
Complements /eval-optimize (automated) by catching tone, intent, and UX
issues that judges cannot measure.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-review diagram](eval-review.svg)
</div>

## Arguments

```bash
/eval-review --run-id <id> [--config <path>] [--cases <name> ...]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--run-id` | :material-check: | - | Which eval run to review. |
| `--config` |  | `auto-discover` | Path to eval config. |
| `--cases` |  | - | Exact case directory names to review (space-separated). Defaults to all cases. |

## Usage

```bash
/eval-review --run-id 2026-05-01-opus
/eval-review --run-id 2026-05-01-opus --cases case-003 case-005
```
