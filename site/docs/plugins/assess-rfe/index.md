---
title: assess-rfe
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-rfe

Assess RFEs against quality criteria using a structured rubric. Supports
single-input mode (Jira key, file, URL, raw text) and bulk mode with
30 concurrent scorer agents and CSV results.


!!! info "Plugin Details"

    - **Version**: 1.0.0
    - **Author**: Jason Greene
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [n1hility/assess-rfe](https://github.com/n1hility/assess-rfe)
    - **Tags**: <span class="tag-pill">rfe</span> <span class="tag-pill">rubric</span> <span class="tag-pill">quality</span> <span class="tag-pill">assessment</span>

## Pipeline

<div class="diagram-container" markdown>
![assess-rfe pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/assess-rfe`](assess-rfe.md) | Assess RFEs against quality criteria using a structured rubric | :material-check: |
| [`/export-rubric`](export-rubric.md) | Export the assessment rubric | :material-check: |

## Installation

```bash
/plugin install assess-rfe@opendatahub-skills
```
