---
title: pipeline-grouping
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-grouping

Groups failed CI/CD pipeline jobs by shared root cause. Reads the
preprocessed `errors.txt` for every failed job listed in the job
manifest, identifies distinct failure patterns, and clusters jobs whose
errors point to the same underlying cause — merging across collections
and pipeline actions when the errors match, splitting within a collection
when they differ (biasing toward splitting when uncertain, since each
group spawns one downstream RCA task).

Rather than emitting JSON directly, the skill drives the `grouper.py`
CLI to build groups incrementally in a work file and then `finalize`s
it, which validates that every expected job ID is assigned to exactly
one group before writing `grouping.json`. If open Jira tickets are
provided in `recent-tickets.json`, it also checks each group against
them and writes `dedup-results.json` for matches, so recurring failures
reuse an existing ticket instead of filing a duplicate.

**Inputs** (from `/workspace/`): `_context/grouping-context.json`,
`jobs/<id>-<name>/errors.txt`, optional `recent-tickets.json`.
**Outputs**: `grouping.json`, optional `dedup-results.json`.

**Plugin**: [pipeline-skills](index.md) | **:material-close: Internal**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Read preprocessed error files for all failed jobs, identify distinct failure patterns, and group jobs by shared root cause into grouping.json.

    **Functions:**

    - `analyze`: Interpret inputs to extract structure, meaning, or implications.

    **Metrics:**

    - `task_success` (`deterministic`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback.

    **Success Conditions:**

    - Produces grouping.json with all expected job IDs assigned to groups.
    - Each group has a human-readable summary and representative error messages.

    **Must Preserve:**

    - Every expected job ID must appear in exactly one group.
    - Do not modify job trace logs or error files.

    **Fixed Context:**

    - **Tools**: `Read`, `Bash`, `Grep`, `Glob`
    - **CLI**: `python3`
    - **Documents**: —
    - **Knowledge Inputs**: `task_input` (task_private)

    **Source Assertions:**

    - **Skill Path**: `skills/pipeline-grouping/SKILL.md`
    - **Supporting Paths**: `skills/pipeline-grouping/scripts/grouper.py`

## Diagram

<div class="diagram-container" markdown>
![pipeline-grouping diagram](pipeline-grouping.svg)
</div>

## Usage

Internal skill (`user-invocable: false`) — invoked by the
[pipeline-failure-analyzer](https://github.com/opendatahub-io/pipeline-failure-analyzer)
orchestrator inside the Claude Code container, not run interactively. The
orchestrator prepares the `/workspace/` inputs and reads back `grouping.json`.
