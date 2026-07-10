---
title: assess-strat
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-strat

Assess RHAISTRAT strategies against quality criteria using a scored rubric with calibration examples. Scores across four dimensions: feasibility, testability, scope, and architecture.

!!! info "Plugin Details"

    - **Version**: 1.0.0
    - **Author**: Eder Ignatowicz
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [opendatahub-io/assess-strat](https://github.com/opendatahub-io/assess-strat)
    - **Tags**: <span class="tag-pill">strategy</span> <span class="tag-pill">strat</span> <span class="tag-pill">rubric</span> <span class="tag-pill">quality</span> <span class="tag-pill">assessment</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/assess-strat`](assess-strat.md) | Assess strategies against quality criteria using a structured rubric | :material-check: |
| [`/export-rubric`](export-rubric.md) | Export the assessment rubric | :material-check: |

## Contract Summary

Headline view only. Individual skill pages carry the detailed measures, references, success conditions, and invariants.

### Focus Functions

- `review` — Assess an artifact against expectations and identify issues, risks, or fit.
- `generate` — Produce a new artifact for the user or another tool to consume.

### Focus Metrics

- `task_success` — Whether the skill completes the intended job correctly for the task. (Prefer deterministic or verifier-backed checks; use judge only as a fallback.)
- `evidence_completeness` — Whether claims and verdicts are backed by enough concrete evidence. (Use verifier-backed checks when evidence can be counted; otherwise use a rubric-backed judge.)
- `output_quality` — Human-judged quality of the final artifact when deterministic checks are insufficient. (Judge only; always pair it with a stable rubric_ref and, when available, calibration data.)
- `latency` — How quickly the skill produces the final usable result. (Deterministic only; measure elapsed wall-clock time for the user-visible outcome.)

### Notes

Strategy assessment against a scored rubric and rubric export.

## Installation

```bash
/plugin install assess-strat@opendatahub-skills
```
