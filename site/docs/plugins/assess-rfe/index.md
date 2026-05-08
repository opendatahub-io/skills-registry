---
title: assess-rfe
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-rfe

Structured quality assessment for RFEs (Requests for Enhancement) against
a five-criteria rubric: WHAT (clear customer need), WHY (business justification
with named customers or revenue data), Open to HOW (leaves architecture to
engineering), Not a Task (business need vs. activity), and Right-Sized (maps
to approximately one strategy feature). Each criterion is scored 0-2 for a
total out of 10, with pass requiring 7+ and no zeros.

Supports single-input mode accepting Jira issue keys (via MCP or REST API
fallback), file paths, URLs, or raw text. Bulk mode fetches all issues from
a Jira project, then dispatches up to 30 concurrent scorer sub-agents that
each apply the identical rubric from a single source-of-truth prompt file.
Results are written as individual markdown files into a timestamped run
directory, then aggregated into a CSV with summary statistics including
pass/fail rates, score distribution, criteria averages, what-if analysis,
and near-miss identification.

The scorer agents run with restricted tool access (Read and Write only) to
prevent prompt injection from untrusted Jira content. The rubric includes
detailed calibration examples for each criterion and a comprehensive list of
established RHOAI platform technologies that are considered vocabulary rather
than architecture prescription.


!!! info "Plugin Details"

    - **Version**: 1.0.0
    - **Author**: Jason Greene
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [n1hility/assess-rfe](https://github.com/n1hility/assess-rfe)
    - **Tags**: <span class="tag-pill">rfe</span> <span class="tag-pill">rubric</span> <span class="tag-pill">quality</span> <span class="tag-pill">assessment</span>

## Pipeline

<div class="diagram-container" markdown>
![assess-rfe pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/assess-rfe`](assess-rfe.md) | Assess RFEs against quality criteria using a structured rubric | :material-check: |
| [`/export-rubric`](export-rubric.md) | Export the assessment rubric | :material-check: |

## Installation

```bash
/plugin install assess-rfe@opendatahub-skills
```

## Architecture

The plugin uses an orchestrator/agent pattern. The main assess-rfe skill acts
as a coordinator that handles input detection, Jira fetching, run directory
management, and agent lifecycle. Individual assessments are delegated to
rfe-scorer sub-agents (defined in agents/rfe-scorer.md) running with minimal
permissions (Read + Write only, acceptEdits permission mode) as a security
boundary against prompt injection from untrusted Jira content.

Bulk mode operates in phases: preflight checks (environment variables, run
state), Jira dump (all issues cached locally), run setup (timestamped
directory with queue file), concurrent agent dispatch (batches of 30 via
next_batch.py), and result aggregation (parse_results.py + summarize_run.py).
Resume support is built in via queue files and symlinked run directories.

Python scripts handle all data operations (Jira API calls, ADF-to-markdown
conversion, queue management, progress tracking, result parsing, CSV
generation, and summary statistics). The coordinator never uses shell pipes
or compound commands, relying instead on structured script output with
key=value parsing.
