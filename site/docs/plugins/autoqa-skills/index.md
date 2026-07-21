---
title: autoqa-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# autoqa-skills

AI skills for AutoQA CI/CD test failure analysis and triage. Covers root cause analysis of test failure logs, matching failures against historical Jira tickets, and classifying failures as known infrastructure false alarms. Designed to run inside a Claude Code container as part of the AutoQA CI pipeline.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Repository**: [opendatahub-io/autoqa-skills](https://github.com/opendatahub-io/autoqa-skills)
    - **Tags**: <span class="tag-pill">ci</span> <span class="tag-pill">test</span> <span class="tag-pill">failure-analysis</span> <span class="tag-pill">triage</span> <span class="tag-pill">jira</span> <span class="tag-pill">autoqa</span> <span class="tag-pill">false-alarm</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/failure-analysis`](failure-analysis.md) | Analyze a CI/CD test failure log to identify the root cause and produce a structured verdict | :material-close: internal |
| [`/failure-matching`](failure-matching.md) | Match a test failure against historical Jira tickets to find known issues | :material-close: internal |
| [`/false-alarm-detection`](false-alarm-detection.md) | Classify a test failure as a known infrastructure false alarm or genuine bug by comparing against pluggable pattern definitions | :material-close: internal |

## Installation

```bash
/plugin install autoqa-skills@opendatahub-skills
```
