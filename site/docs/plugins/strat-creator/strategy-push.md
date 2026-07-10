---
title: strategy-push
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-push

Push a locally-refined strategy back to Jira and resubmit to CI

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Push an improved strategy back to Jira and resubmit it to CI for re-evaluation.

    **Functions:**

    - `execute`: Carry out a bounded operational task in tools, CLIs, or external systems.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.

    **Success Conditions:**

    - Updates the Jira issue description with refined strategy content.
    - Removes needs-attention label and resubmits for CI processing.

    **Must Preserve:**

    - Only push strategies with strat-creator-needs-attention label.
    - Do not push strategies that have not been locally modified.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-push/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-push
```
