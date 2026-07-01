---
title: pipeline-rca
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-rca

Performs root cause analysis for a single error group produced by
pipeline-grouping. Reads the group's trace logs and preprocessed errors,
investigates the failure against pipeline source at the exact commit SHA
(local git first, GitLab API fallback), and diagnoses *why* the failure
occurred rather than just what it looks like.

The skill is disciplined about evidence: it focuses on the first error
in each log (later errors are cascades), verifies its theory with a
cheap distinguishing check before committing to a diagnosis, lowers
confidence when verification isn't possible, and redacts credentials in
any quoted log lines. It emits content-fragment section files —
`error-overview.md` (symptom), `root-cause.md` (diagnosis and failure
chain), and optionally `resolution.md` and `feedback.md` — plus a
schema-validated `finding.json` carrying the confidence level, cascade
flag, group consistency, target repository for the fix, and every file
consulted. A deterministic outer script assembles these into the
per-group report.

**Inputs** (from `/workspace/`): `_context/rca-context.json`,
`pipeline-context.json`, `groups/<group_id>/jobs/.../trace.log` and
`errors.txt`, `_repos/` shallow clones. **Outputs**:
`<group_dir>/finding.json` and `<group_dir>/sections/*.md`.

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

## Diagram

<div class="diagram-container" markdown>
![pipeline-rca diagram](pipeline-rca.svg)
</div>

## Usage

Internal skill (`user-invocable: false`) — invoked once per error group by the
[pipeline-failure-analyzer](https://github.com/opendatahub-io/pipeline-failure-analyzer)
orchestrator inside the Claude Code container, not run interactively. A
deterministic outer script assembles the section files and `finding.json`
into the per-group report.
