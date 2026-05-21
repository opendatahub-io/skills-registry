---
title: meeting-risk-agenda
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# meeting-risk-agenda

Analyzes pre-meeting updates and generates a risk-focused agenda by
classifying each update into Blocked, At Risk, or No Issues categories.
Detects risk signals such as "blocked", "stuck", "waiting", "dependency",
lack of progress, and unclear ownership. Extracts owner names when present
and organizes the agenda with blocked items first, at-risk items second,
and no-issues items deprioritized or summarized.

If no risks are found, the skill suggests the meeting may not be necessary
or could be shortened. If ownership is unclear, it explicitly calls that out.

**Plugin**: [meeting-quality-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![meeting-risk-agenda diagram](meeting-risk-agenda.svg)
</div>

## Arguments

```bash
/meeting-risk-agenda [meeting_title] <update_document> [attendee_list]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `meeting_title` |  | - | Title of the meeting (optional context) |
| `update_document` | :material-check: | - | Meeting update document content (Google Doc or pasted text) |
| `attendee_list` |  | - | List of meeting attendees (optional, helps with owner matching) |

## Usage

```bash
/meeting-risk-agenda
Build a focused agenda from our team's weekly updates
```
