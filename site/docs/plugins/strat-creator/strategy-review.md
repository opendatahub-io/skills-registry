---
title: strategy-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-review

Adversarial review with rubric scoring and independent forked reviewers

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Score a strategy against the rubric and run independent forked reviewers for detailed adversarial prose.

    **Functions:**

    - `review`: Assess an artifact against expectations and identify issues, risks, or fit.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-review/SKILL.md`
    - `output_quality` (`judge`): Human-judged quality of the final artifact when deterministic checks are insufficient. Guidance: Judge only; always pair it with a stable rubric_ref and, when available, calibration data. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-review/SKILL.md`

    **Success Conditions:**

    - Produces a review file with numeric scores across all rubric dimensions.
    - Runs independent reviewer agents for feasibility, testability, scope, and architecture.

    **Must Preserve:**

    - Do not skip rubric criteria or invent findings not supported by evidence.
    - Do not modify the strategy being reviewed.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `Skill`, `Agent`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private), `tool_output` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-review/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-review
```
