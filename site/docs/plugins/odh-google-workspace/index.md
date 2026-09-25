---
title: odh-google-workspace
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-google-workspace

Gmail, Google Calendar, Docs, and Drive integration

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">google-workspace</span> <span class="tag-pill">gmail</span> <span class="tag-pill">calendar</span> <span class="tag-pill">drive</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/email-meeting-summary`](email-meeting-summary.md) | Use when the user wants to summarize a Google Meet meeting and send the summary by email. Reviews a Google Meet transcript for a specific meeting topic, then composes a Gmail draft summarizing decisions and action items for that topic. Prompts for meeting selection if not specified, and for topic selection before drafting. Stops with a message if the transcript is not yet available. | :material-check: |
| [`/gmail-draft`](gmail-draft.md) | Use this skill to compose a Gmail draft from text content in the conversation. Accepts a body, recipient list, and subject — either from the user or from context — and creates a draft in the user's Gmail Drafts folder via gws. | :material-check: |
| [`/google-workspace`](google-workspace.md) | Fetch and query data from Google Workspace using the gws CLI — Gmail, Calendar, Docs, Sheets, Slides, and Drive. Use this skill whenever the user mentions email, inbox, messages, calendar, meetings, schedule, agenda, Google Docs, spreadsheets, presentations, or Drive files. Trigger on phrases like "check my email", "what meetings do I have", "read this doc", "open this spreadsheet", "find files in Drive", or any Google URL (docs.google.com, drive.google.com). | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-google-workspace@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-google-workspace` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
