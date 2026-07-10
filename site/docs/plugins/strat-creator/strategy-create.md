---
title: strategy-create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-create

Create strategies from approved RFEs by cloning them to RHAISTRAT in Jira

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Clone approved RFEs into the RHAISTRAT Jira project and set up local artifacts for refinement.

    **Functions:**

    - `execute`: Carry out a bounded operational task in tools, CLIs, or external systems.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-create/SKILL.md`

    **Success Conditions:**

    - Creates RHAISTRAT issues from approved RFEs via Jira clone or manual creation.
    - Writes local strategy stubs to artifacts/strat-tasks/ with correct frontmatter.

    **Must Preserve:**

    - Do not clone RFEs that have not been approved.
    - Do not modify the source RFE issue in Jira.

    **Fixed Context:**

    - **Tools**: `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`, `AskUserQuestion`, `mcp__atlassian__searchJiraIssuesUsingJql`, `mcp__atlassian__getJiraIssue`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private), `tool_output` (task_private)

    **Source Assertions:**

    - **Skill Path**: `.claude/skills/strategy-create/SKILL.md`
    - **Supporting Paths**: —

## Usage

```bash
/strategy-create
```
