---
title: test-plan-create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-create

Generate a complete test plan for a RHOAI feature from a Jira strategy
(RHAISTRAT or RHOAIENG issue), with optional ADR for additional technical depth.
Spawns 3 parallel sub-analyzers (endpoints, risks, infra), merges their findings
into a structured template, collects gaps into TestPlanGaps.md, then runs an
automated quality review with scoring and up to 2 auto-revision cycles. Produces
TestPlan.md, TestPlanGaps.md, TestPlanReview.md, and README.md in a feature directory.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-create diagram](test-plan-create.svg)
</div>

## Arguments

```bash
/test-plan-create <JIRA_KEY> [ADR_FILE_PATH]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `JIRA_KEY` | :material-check: | - | Jira strategy key (RHAISTRAT-*) or issue key (RHOAIENG-*) to generate the test plan from |
| `ADR_FILE_PATH` |  | - | Local path to an ADR document (markdown, text, or PDF) for additional technical depth |
| `--output-dir` |  | - | Override output directory for test plan artifacts (skips validation) |

## Usage

```bash
/test-plan-create RHAISTRAT-400
/test-plan-create RHOAIENG-48676
/test-plan-create RHAISTRAT-400 /path/to/adr.pdf
```
