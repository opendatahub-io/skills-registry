---
title: assess-strat
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-strat

Assess strategies against quality criteria using a structured rubric

**Plugin**: [assess-strat](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Score a strategy against the published rubric and explain the result.

    **Functions:**

    - `review`: Assess an artifact against expectations and identify issues, risks, or fit.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/assess-strat@ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b:skills/assess-strat/SKILL.md`
    - `evidence_completeness` (`judge`): Whether claims and verdicts are backed by enough concrete evidence. Guidance: Use verifier-backed checks when evidence can be counted; otherwise use a rubric-backed judge. References: rubric_ref=`opendatahub-io/assess-strat@ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b:skills/assess-strat/SKILL.md`
    - `output_quality` (`judge`): Human-judged quality of the final artifact when deterministic checks are insufficient. Guidance: Judge only; always pair it with a stable rubric_ref and, when available, calibration data. References: rubric_ref=`opendatahub-io/assess-strat@ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b:skills/assess-strat/SKILL.md`

    **Success Conditions:**

    - Produces a complete rubric-based assessment for the supplied strategy input.
    - Includes evidence-backed scoring rationale for each criterion.

    **Must Preserve:**

    - Do not skip rubric criteria or invent unsupported evidence.
    - Do not change the accepted input modes declared by the skill.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `Agent`, `TaskGet`, `mcp__atlassian__getJiraIssue`, `mcp__atlassian__searchJiraIssuesUsingJql`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private), `tool_output` (task_private)

    **Source Assertions:**

    - **Skill Path**: `skills/assess-strat/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/assess-strat
```
