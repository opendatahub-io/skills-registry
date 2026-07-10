---
title: strategy-pull
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-pull

Pull a post-CI strategy from Jira into local workspace for human review

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Pull a RHAISTRAT issue from Jira into local/ workspace for human review and iteration.

    **Functions:**

    - `retrieve`: Locate and return source material, facts, or artifacts needed for later work.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.

    **Success Conditions:**

    - Writes the strategy content to local/strat-tasks/ with correct frontmatter.
    - Pulls associated reviews and RFE originals into local/ subdirectories.

    **Must Preserve:**

    - Do not modify the Jira issue during pull.
    - Do not overwrite local files without user confirmation.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Bash`, `Glob`, `Grep`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-pull/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-pull
```
