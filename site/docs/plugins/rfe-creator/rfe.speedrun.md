---
title: rfe.speedrun
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.speedrun

Execute the full RFE pipeline end-to-end: create, auto-fix (review +
revise + split), and submit. Supports three modes: batch YAML input
(multiple ideas in a file), existing Jira keys, or a single free-text
idea. In batch mode, pre-allocates all RFE IDs and launches parallel
create agents. Orchestrates by invoking rfe.create, rfe.auto-fix, and
rfe.submit as sub-skills.

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
| `--batch-size` |  | `5` | Override batch size for auto-fix phase |
| `--announce-complete` |  | - | Print completion marker when done (for CI/eval harnesses) |

## Usage

```bash
/rfe.speedrun Better dashboard for ML model monitoring
/rfe.speedrun RHAIRFE-1234
/rfe.speedrun --input batch.yaml --headless --dry-run
/rfe.speedrun --input batch.yaml --headless --batch-size 10 --announce-complete
```
