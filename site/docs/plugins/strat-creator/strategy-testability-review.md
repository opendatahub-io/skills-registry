---
title: strategy-testability-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-testability-review

Reviews strategy for testability and measurable acceptance criteria

**Plugin**: [strat-creator](index.md) | **:material-close: Internal**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Review strategy features for testability — measurable acceptance criteria, edge case coverage, and validation feasibility.

    **Functions:**

    - `review`: Assess an artifact against expectations and identify issues, risks, or fit.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-testability-review/SKILL.md`

    **Success Conditions:**

    - Produces a testability assessment for each strategy with recommendation.
    - Identifies untestable criteria and missing edge cases.

    **Must Preserve:**

    - Do not approve strategies with unmeasurable acceptance criteria.
    - Do not invent test scenarios unsupported by the strategy content.

    **Fixed Context:**

    - **Tools**: `Read`, `Grep`, `Glob`
    - **CLI**: —
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-testability-review/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-testability-review
```
