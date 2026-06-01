---
title: SPIKE-executor
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# SPIKE-executor

Execute RHOAI SPIKE investigations through a 9-step human-in-the-loop
lifecycle. Each step produces artifacts in the artifacts/ directory and
pauses at a breakpoint for explicit user approval before continuing.
Steps: (1) intake, (2) plan generation, (3) Jira preview, (4) Jira
creation, (5) AI research enrichment with hallucination validation,
(6) test plan + pytest suite generation, (7) test execution + rubric
scoring, (8) RFE generation + approval, (9) completion summary. Supports
--skip-tests (no OpenShift) and --skip-jira (no Jira credentials).

**Plugin**: [spike-executor](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![SPIKE-executor diagram](SPIKE-executor.svg)
</div>

## Arguments

```bash
/SPIKE-executor <project> [--skip-tests] [--skip-jira]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `project` | :material-check: | - | Name of the project/technology being investigated (e.g., AutoGluon, gRPC). Used as the suffix for all artifact filenames. |
| `--skip-tests` |  | - | Skip cluster tests and scoring (Steps 6-7). For environments without OpenShift access. |
| `--skip-jira` |  | - | Skip Jira sync steps (Steps 3-4, 5b). For testing without Jira credentials. |

## Usage

```bash
/SPIKE-executor AutoGluon
/SPIKE-executor gRPC --skip-tests
/SPIKE-executor my-project --skip-jira
```
