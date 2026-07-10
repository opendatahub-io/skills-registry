---
title: export-rubric
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# export-rubric

Export the scoring rubric to artifacts/strat-rubric.md

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Export the strat-creator scoring rubric to artifacts/strat-rubric.md in the current working directory.

    **Functions:**

    - `generate`: Produce a new artifact for the user or another tool to consume.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.
    - `latency` (`deterministic`): How quickly the skill produces the final usable result. Guidance: Deterministic only; measure elapsed wall-clock time for the user-visible outcome.

    **Success Conditions:**

    - Writes artifacts/strat-rubric.md under the current working directory.
    - Confirms the file was written and prints its path.

    **Must Preserve:**

    - Do not modify the rubric content while exporting it.
    - Do not redirect the export to a path other than artifacts/strat-rubric.md.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Bash`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/export-rubric/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/export-rubric
```
