---
title: strategy-feasibility-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-feasibility-review

Reviews strategy for technical feasibility and effort estimate credibility

**Plugin**: [strat-creator](index.md) | **:material-close: Internal**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Review strategy features for technical feasibility, implementation complexity, and effort estimate credibility.

    **Functions:**

    - `review`: Assess an artifact against expectations and identify issues, risks, or fit.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-feasibility-review/SKILL.md`

    **Success Conditions:**

    - Produces a feasibility assessment for each strategy with recommendation.
    - Grounds findings in architecture context when available.

    **Must Preserve:**

    - Do not approve strategies with fundamental technical flaws.
    - Do not fabricate architecture constraints not present in the docs.

    **Fixed Context:**

    - **Tools**: `Read`, `Grep`, `Glob`
    - **CLI**: —
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-feasibility-review/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-feasibility-review
```
