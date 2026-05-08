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

## Diagram

<div class="diagram-container" markdown>
![assess-rfe diagram](assess-rfe.svg)
</div>

## Arguments

```
/assess-rfe <input>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `input` | :material-check: | — | The RFE to assess. Accepts multiple formats: a Jira issue key (e.g., RHAIRFE-1234), a file path to a document, a URL, raw pasted text, or a wildcard pattern (e.g., RHAIRFE-*) for bulk assessment of an entire Jira project.
 |

## Usage

```
/assess-rfe RHAIRFE-1234
/assess-rfe PROJ-99
/assess-rfe /path/to/document.md
/assess-rfe https://some-url
/assess-rfe <paste raw text>
/assess-rfe RHAIRFE-*
```
