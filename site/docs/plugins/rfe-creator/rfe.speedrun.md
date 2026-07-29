---
title: rfe.speedrun
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.speedrun

Execute the full RFE pipeline end-to-end -- create, auto-fix (review +
revise + split), and submit -- with minimal interaction. Detects one of
three modes: batch YAML input (multiple ideas in a file), one or more
existing Jira keys, or a single free-text idea. In batch mode it validates
the input file with validate_batch_input.py --strict before spending any
agent budget, pre-allocates all RFE IDs, and launches one parallel
rfe.create agent per entry. It always passes an explicit --batch-size to
auto-fix for reproducibility, then verifies completeness with
check_autofix_complete.py and re-invokes auto-fix on any missing IDs (up to
3 retries). Orchestrates purely by invoking rfe.create, rfe.auto-fix, and
rfe.submit, persisting config and IDs to disk between phases to survive
context compression.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.speedrun diagram](rfe.speedrun.svg)
</div>

## Arguments

```bash
/rfe.speedrun <idea-or-key> [--input <path>] [--headless] [--dry-run] [--batch-size N] [--announce-complete]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `idea-or-key` |  | - | A free-text idea or Jira key (RHAIRFE-NNNN). Mutually exclusive with --input. |
| `--input` |  | - | Path to a YAML file with batch entries (prompt, priority, labels per entry) |
| `--headless` |  | - | Suppress questions and confirmations (for CI/eval) |
| `--dry-run` |  | - | Skip Jira writes in submit phase |
| `--batch-size` |  | `5` | Override batch size for auto-fix phase (always passed through explicitly) |
| `--announce-complete` |  | - | Print completion marker when done (for CI/eval harnesses) |

## Usage

```bash
/rfe.speedrun Better dashboard for ML model monitoring
/rfe.speedrun RHAIRFE-1234
/rfe.speedrun --input batch.yaml --headless --dry-run
/rfe.speedrun --input batch.yaml --headless --batch-size 10 --announce-complete
```
