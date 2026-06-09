---
title: eval-optimize
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-optimize

Automated skill improvement loop that acts autonomously (no per-case human
input). Runs evaluation, identifies judge failures from summary.yaml, reads
execution transcripts and failing case outputs via Explore sub-agents to
trace root causes to specific SKILL.md instructions, makes surgical edits
grounded in evidence, re-runs evaluation with regression baseline checks
(targeting failing cases first, then a full run), handles regressions
(continue if minor, revert if major), and iterates up to a configurable
maximum. Also reads human feedback from review.yaml (from /eval-review) and
MLflow annotations to prioritize issues flagged by humans over automated judge
failures. Never edits judges, eval.yaml, or builtin judge code -- only the
skill under test. Stops when all judges pass or max iterations is reached, then
suggests logging results to MLflow.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-optimize diagram](eval-optimize.svg)
</div>

## Arguments

```bash
/eval-optimize [--config <path>] [--model <model>] [--max-iterations <N>] [--run-id <id>] [--target-judge <name>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--config` |  | `auto-discover` | Path to eval config. |
| `--model` |  | `models.skill from config` | Model for skill execution. Pass the same model on every iteration for comparable results. |
| `--max-iterations` |  | `3` | Maximum optimization iterations before stopping. |
| `--run-id` |  | `auto-generated` | Base run ID. Iterations append -iter-N. |
| `--target-judge` |  | - | Focus optimization on a specific failing judge instead of all judges. |

## Usage

```bash
/eval-optimize
/eval-optimize --max-iterations 5 --model claude-opus-4-6
/eval-optimize --target-judge completeness
```
