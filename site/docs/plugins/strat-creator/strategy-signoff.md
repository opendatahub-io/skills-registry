---
title: strategy-signoff
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-signoff

Sign off on a CI-approved strategy with human sign-off label

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Sign off on a CI-approved strategy by pushing final content and adding the human-sign-off label.

    **Functions:**

    - `execute`: Carry out a bounded operational task in tools, CLIs, or external systems.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.

    **Success Conditions:**

    - Adds strat-creator-human-sign-off label to the Jira issue.
    - Confirms the strategy has passed CI rubric before sign-off.

    **Must Preserve:**

    - Do not sign off strategies that have not passed CI review.
    - Do not remove existing labels during sign-off.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-signoff/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-signoff
```
