<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-run

Execute a skill against test cases, collect artifacts, score with inline and
LLM judges, detect regressions against a baseline, and generate an HTML report.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-run diagram](eval-run.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--config` |  | `eval.yaml` | Path to eval config |
| `--model` |  | `models.skill from config` | Model for skill execution |
| `--subagent-model` |  | — | Model for subagents (falls back to skill model) |
| `--judge-model` |  | `models.judge from config` | Model for LLM judges |
| `--baseline` |  | — | Compare against a previous run for regression detection |
| `--cases` |  | — | Filter cases by glob pattern (e.g. case-001*) |
| `--no-judge` |  | — | Skip judge scoring (execution only) |
| `--gold` |  | — | Save outputs as gold references |

## Usage

```
/eval-run
/eval-run --model claude-opus-4-6 --baseline 2026-05-01
/eval-run --cases 'case-001*' --no-judge
```
