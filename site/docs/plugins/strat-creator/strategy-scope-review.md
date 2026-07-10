---
title: strategy-scope-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-scope-review

Reviews strategy for right-sizing and bounded scope

**Plugin**: [strat-creator](index.md) | **:material-close: Internal**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Review strategy features for scope — right-sizing, bounded deliverables, and effort-to-scope alignment.

    **Functions:**

    - `review`: Assess an artifact against expectations and identify issues, risks, or fit.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-scope-review/SKILL.md`

    **Success Conditions:**

    - Produces a scope assessment for each strategy with recommendation.
    - Flags strategies that are too large to deliver or too small to warrant a strategy.

    **Must Preserve:**

    - Do not approve strategies with unbounded scope.
    - Do not split or merge strategies without justification from effort estimates.

    **Fixed Context:**

    - **Tools**: `Read`, `Grep`, `Glob`
    - **CLI**: —
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-scope-review/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-scope-review
```
