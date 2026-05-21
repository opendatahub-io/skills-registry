---
title: meeting-async-update-check
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# meeting-async-update-check

Checks a shared pre-meeting update document and identifies attendees who
have not provided an async update before a status meeting. For each
attendee, the skill determines whether they appear to have contributed by
looking for section headers with their name, email alias references, or
attributed bullet lists. When the document contains Jira-exported content,
it attempts to identify owners from Assignee/Owner fields and marks
ambiguous items as uncertain.

Produces three sections: attendees with updates, attendees missing updates,
and uncertain matches needing organizer review. Also drafts a professional
reminder message the organizer can send to those who haven't updated yet.

**Plugin**: [meeting-quality-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![meeting-async-update-check diagram](meeting-async-update-check.svg)
</div>

## Arguments

```bash
/meeting-async-update-check <meeting_title> <meeting_datetime> <attendee_list> <update_document> [update_format]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `meeting_title` | :material-check: | - | Title of the meeting being checked |
| `meeting_datetime` | :material-check: | - | Date and time of the upcoming meeting |
| `attendee_list` | :material-check: | - | List of meeting attendees to check for updates |
| `update_document` | :material-check: | - | Shared meeting update document content or link (Google Doc or pasted text) |
| `update_format` |  | - | Optional expected format for updates, if one exists |

## Usage

```bash
/meeting-async-update-check
Check who hasn't updated the weekly sync doc yet
```
