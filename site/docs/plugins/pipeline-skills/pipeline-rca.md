---
title: pipeline-rca
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-rca

Root cause analysis for a pipeline failure error group with structured findings and section files

**Plugin**: [pipeline-skills](index.md) | **:material-close: Internal**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Investigate the root cause of a CI/CD failure group by analyzing trace logs, source code, and build artifacts. Produce structured section files and a finding.json with classification metadata.

    **Functions:**

    - `analyze`: Interpret inputs to extract structure, meaning, or implications.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.

    **Success Conditions:**

    - Produces finding.json with all required fields valid against the schema.
    - Produces sections/error-overview.md and sections/root-cause.md.

    **Must Preserve:**

    - Do not fabricate log lines or error messages not present in the evidence.
    - Redact credentials, tokens, and API keys in all output.

    **Fixed Context:**

    - **Tools**: `Read`, `Bash`, `Grep`, `Glob`
    - **CLI**: `python3`, `git`, `glab`
    - **Documents**: —
    - **Knowledge Inputs**: `repository_content` (public), `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `skills/pipeline-rca/SKILL.md`
    - **Supporting Paths**: `skills/pipeline-rca/references/finding.schema.json`, `skills/pipeline-rca/references/error-overview-section-template.md`, `skills/pipeline-rca/references/rca-section-template.md`, `skills/pipeline-rca/references/resolution-section-template.md`

## Usage

```bash
/pipeline-rca
```
