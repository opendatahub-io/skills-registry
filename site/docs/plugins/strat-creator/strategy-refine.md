---
title: strategy-refine
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-refine

Refine a strategy with technical HOW, dependencies, and NFRs

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Refine a strategy stub into a complete strategy with technical approach, dependencies, impacted teams, and NFRs.

    **Functions:**

    - `transform`: Rewrite or convert existing input into a different form while preserving intent.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-refine/SKILL.md`

    **Success Conditions:**

    - Produces a refined strategy with HOW, dependencies, and NFRs grounded in platform architecture.
    - Updates the local strategy artifact with complete frontmatter and structured sections.

    **Must Preserve:**

    - Do not alter the original RFE scope or acceptance criteria.
    - Do not fabricate component names or dependencies not present in the architecture context.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private), `tool_output` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-refine/SKILL.md`
    - **Supporting Paths**: `.claude/skills/strategy-refine/strat-template.md`

## Usage

```bash
/strategy-refine
```
