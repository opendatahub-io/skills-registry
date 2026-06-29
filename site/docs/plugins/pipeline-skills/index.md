---
title: pipeline-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-skills

Pipeline failure analysis skills for AIPCC CI/CD pipelines. Groups failed jobs by shared root cause using preprocessed error logs, then performs root cause analysis per group with structured findings, section files, and confidence-rated diagnoses. Designed to run inside a Claude Code container as part of the pipeline-failure-analyzer CI pipeline.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [opendatahub-io/pipeline-skills](https://github.com/opendatahub-io/pipeline-skills)
    - **Tags**: <span class="tag-pill">pipeline</span> <span class="tag-pill">ci-cd</span> <span class="tag-pill">failure-analysis</span> <span class="tag-pill">grouping</span> <span class="tag-pill">root-cause</span> <span class="tag-pill">gitlab</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/pipeline-grouping`](pipeline-grouping.md) | Group failed CI/CD pipeline jobs by error similarity using log analysis and Jira ticket deduplication | :material-close: internal |
| [`/pipeline-rca`](pipeline-rca.md) | Root cause analysis for a pipeline failure error group with structured findings and section files | :material-close: internal |

## Installation

```bash
/plugin install pipeline-skills@opendatahub-skills
```
