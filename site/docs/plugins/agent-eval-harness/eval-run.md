---
title: eval-run
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-run

Executes a skill against test cases, collects artifacts, scores with judges,
and generates an HTML report. Orchestrates via scripts: preflight checks for
stale artifacts, workspace creation with isolated per-case directories, headless
skill execution (case mode: once per case; batch mode: single invocation),
artifact collection into per-case dirs, scoring with inline checks and LLM
judges, optional pairwise comparison against a baseline for regression detection,
and report generation. Supports concurrent case execution via parallelism setting,
tool interception for AskUserQuestion and external APIs, and configurable
reasoning effort levels.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-run diagram](eval-run.svg)
</div>

## Arguments

```bash
/eval-run [--config <path>] [--model <model>] [--run-id <id>] [--baseline <run-id>] [--case <filter>] [--no-judge] [--gold] [--effort <level>] [--subagent-model <model>] [--skill <name>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--config` |  | `eval.yaml` | Path to eval config. |
| `--model` |  | `models.skill from config` | Model for skill execution. Required if models.skill is unset in eval.yaml. |
| `--subagent-model` |  | `models.subagent, falls back to skill model` | Model for subagents (e.g., claude-sonnet-4-6 while main is claude-opus-4-7). |
| `--run-id` |  | `YYYY-MM-DD-<model>` | Identifier for this run. |
| `--case` |  | - | Substring match to select specific cases. |
| `--baseline` |  | - | Previous run to compare against for regression detection via pairwise comparison. |
| `--no-judge` |  | `false` | Skip LLM judges, run inline checks only. |
| `--gold` |  | `false` | Save outputs as gold references after the run. |
| `--effort` |  | `runner.effort from config` | Claude Code reasoning effort level. |
| `--skill` |  | `from config` | Override the skill to test. |

## Usage

```bash
/eval-run --model claude-opus-4-6
/eval-run --model claude-opus-4-6 --baseline 2026-05-01-opus
/eval-run --case case-001 --no-judge
/eval-run --gold
```
