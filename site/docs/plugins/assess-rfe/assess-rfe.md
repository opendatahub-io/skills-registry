---
title: assess-rfe
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-rfe

Assess RFEs against quality criteria using a structured five-criteria
rubric (WHAT, WHY, HOW, Not a Task, Right-Sized) scored 0-2 each for
a total out of 10. Supports single-input mode (Jira issue key via MCP
or REST API, file path, URL, or raw text) and bulk mode (wildcard
pattern like RHAIRFE-*) with up to 30 concurrent parallel scorer
sub-agents. Bulk mode includes phased execution with preflight checks,
Jira project dump, timestamped run directories with resume support,
queue-based batch dispatching, and CSV result aggregation with summary
statistics (pass/fail rates, score distribution, criteria averages,
what-if analysis, and near-miss identification).

**Plugin**: [assess-rfe](index.md) | **:material-check: User-invocable**

## Contract

!!! info "Skill Contract"

    **Version**: `canonical-skill-v1`

    **Problem Statement**: Score an RFE against the published rubric and explain the result.

    **Functions:**

    - `review`: Assess an artifact against expectations and identify issues, risks, or fit.

    **Metrics:**

    - `task_success` (`judge`): Whether the skill completes the intended job correctly for the task. Guidance: Prefer deterministic or verifier-backed checks; use judge only as a fallback. References: rubric_ref=`n1hility/assess-rfe@main:scripts/agent_prompt.md`
    - `evidence_completeness` (`judge`): Whether claims and verdicts are backed by enough concrete evidence. Guidance: Use verifier-backed checks when evidence can be counted; otherwise use a rubric-backed judge. References: rubric_ref=`n1hility/assess-rfe@main:scripts/agent_prompt.md`
    - `output_quality` (`judge`): Human-judged quality of the final artifact when deterministic checks are insufficient. Guidance: Judge only; always pair it with a stable rubric_ref and, when available, calibration data. References: rubric_ref=`n1hility/assess-rfe@main:scripts/agent_prompt.md`

    **Success Conditions:**

    - Produces a complete rubric-based assessment for the supplied RFE input.
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

    - **Skill Path**: `skills/assess-rfe/SKILL.md`
    - **Supporting Paths**: `scripts/agent_prompt.md`

## Diagram

<div class="diagram-container" markdown>
![assess-rfe diagram](assess-rfe.svg)
</div>

## Arguments

```bash
/assess-rfe <input>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `input` | :material-check: | - | The RFE to assess. Accepts multiple formats: a Jira issue key (e.g., RHAIRFE-1234), a file path to a document, a URL, raw pasted text, or a wildcard pattern (e.g., RHAIRFE-*) for bulk assessment of an entire Jira project. |

## Usage

```bash
/assess-rfe RHAIRFE-1234
/assess-rfe PROJ-99
/assess-rfe /path/to/document.md
/assess-rfe https://some-url
/assess-rfe <paste raw text>
/assess-rfe RHAIRFE-*
```
