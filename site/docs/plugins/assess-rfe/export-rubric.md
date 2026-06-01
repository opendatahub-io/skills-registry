---
title: export-rubric
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# export-rubric

Export the assess-rfe scoring rubric to artifacts/rfe-rubric.md in the
current working directory. Useful for reviewing the rubric criteria,
calibration examples, and scoring guidelines outside of an assessment
context, or for sharing the rubric with team members who want to
understand how RFEs are evaluated.

**Plugin**: [assess-rfe](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Export the assess-rfe scoring rubric to artifacts/rfe-rubric.md in the current working directory.

    **Functions:**

    - `generate`: Produce a new artifact for the user or another tool to consume.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.
    - `latency` (`deterministic`): How quickly the skill produces the final usable result. Guidance: Deterministic only; measure elapsed wall-clock time for the user-visible outcome.

    **Success Conditions:**

    - Writes artifacts/rfe-rubric.md under the current working directory.
    - Confirms the file was written and prints its path.

    **Must Preserve:**

    - Do not modify the rubric content while exporting it.
    - Do not redirect the export to a path other than artifacts/rfe-rubric.md under the invocation working directory.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Bash`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `skills/export-rubric/SKILL.md`
    - **Supporting Paths**: `scripts/export_rubric.py`

## Diagram

<div class="diagram-container" markdown>
![export-rubric diagram](export-rubric.svg)
</div>

## Usage

```bash
/export-rubric
```
