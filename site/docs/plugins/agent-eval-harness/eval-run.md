---
title: eval-run
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-run

Executes a skill against test cases, collects artifacts, scores with judges,
and generates an HTML report. Orchestrates via scripts: preflight checks for
stale artifacts, workspace creation with isolated per-case directories,
resolution of tool-interception handlers, headless skill execution (case
mode: once per case with case-specific arguments; batch mode: single
invocation via batch.yaml), artifact collection into per-case dirs, scoring
with four judge types (builtin, inline checks, LLM prompts, external
modules), optional pairwise comparison against a baseline for regression
detection, and report generation. Supports concurrent case execution via the
parallelism setting, tool interception for AskUserQuestion and external APIs,
configurable reasoning effort, and a --gold flag to save outputs as gold
references. Background-launches execute.py and monitors progress; persists
state via state.py and leads its analysis with a decisive recommendation.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-run diagram](eval-run.svg)
</div>

## Arguments

```bash
/eval-run [--config <path>] [--model <model>] [--run-id <id>] [--baseline <run-id>] [--cases <id> ...] [--no-llm-judges] [--gold] [--effort <level>] [--subagent-model <model>] [--skill <name>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--config` |  | `auto-discover` | Path to eval config. If missing, bootstraps via /eval-analyze. |
| `--model` |  | `models.skill from config` | Model for skill execution. Required if models.skill is unset in eval.yaml. |
| `--subagent-model` |  | `models.subagent, falls back to skill model` | Model for subagents (e.g., claude-sonnet-4-6 while main is claude-opus-4-7). |
| `--run-id` |  | `YYYY-MM-DD-<model>` | Identifier for this run. |
| `--cases` |  | - | Exact case IDs to run (space-separated). Defaults to all cases. |
| `--baseline` |  | - | Previous run to compare against for regression detection via pairwise comparison. Must exist under the same eval-name directory. |
| `--no-llm-judges` |  | `false` | Skip LLM judges (prompt, prompt_file, LLM builtins). Run deterministic judges only (check, Python builtins, external code). |
| `--gold` |  | `false` | Save collected outputs as gold reference files in the dataset case dirs after the run. |
| `--effort` |  | `runner.effort from config` | Claude Code reasoning effort level (Claude Code only; ignored by other runners). |
| `--skill` |  | `from config` | Override the skill to test. |

## Usage

```bash
/eval-run --model claude-opus-4-6
/eval-run --model claude-opus-4-6 --baseline 2026-05-01-opus
/eval-run --cases case-001 case-002 --no-llm-judges
/eval-run --gold
```
