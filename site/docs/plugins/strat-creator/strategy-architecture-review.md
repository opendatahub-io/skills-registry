---
title: strategy-architecture-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-architecture-review

Reviews strategy for architectural correctness and integration patterns

**Plugin**: [strat-creator](index.md) | **:material-close: Internal**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Review strategy features for architectural correctness — dependencies, integration patterns, and component interactions.

    **Functions:**

    - `review`: Assess an artifact against expectations and identify issues, risks, or fit.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-architecture-review/SKILL.md`

    **Success Conditions:**

    - Produces an architecture assessment for each strategy with recommendation.
    - Grounds every finding in architecture docs with specific component and API citations.

    **Must Preserve:**

    - Do not approve strategies with incorrect dependency assumptions.
    - Do not flag concerns without citing specific architecture documentation.

    **Fixed Context:**

    - **Tools**: `Read`, `Grep`, `Glob`
    - **CLI**: —
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-architecture-review/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-architecture-review
```
