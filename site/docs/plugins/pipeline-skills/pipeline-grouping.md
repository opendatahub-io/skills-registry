---
title: pipeline-grouping
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-grouping

Group failed CI/CD pipeline jobs by error similarity using log analysis and Jira ticket deduplication

**Plugin**: [pipeline-skills](index.md) | **:material-close: Internal**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Read preprocessed error files for all failed jobs, identify distinct failure patterns, and group jobs by shared root cause into grouping.json.

    **Functions:**

    - `analyze`: Interpret inputs to extract structure, meaning, or implications.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.

    **Success Conditions:**

    - Produces grouping.json with all expected job IDs assigned to groups.
    - Each group has a human-readable summary and representative error messages.

    **Must Preserve:**

    - Every expected job ID must appear in exactly one group.
    - Do not modify job trace logs or error files.

    **Fixed Context:**

    - **Tools**: `Read`, `Bash`, `Grep`, `Glob`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `skills/pipeline-grouping/SKILL.md`
    - **Supporting Paths**: `skills/pipeline-grouping/scripts/grouper.py`

## Usage

```bash
/pipeline-grouping
```
