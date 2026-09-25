---
title: odh-jira
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-jira

Jira ticket management, search, triage, and automation

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">jira</span> <span class="tag-pill">acli</span> <span class="tag-pill">triage</span> <span class="tag-pill">automation</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/acli-setup-check`](acli-setup-check.md) | Verify acli installation and authentication. Checks if acli is installed, authenticated to Jira, and can query projects. Use when troubleshooting acli issues or setting up acli for the first time. | :material-check: |
| [`/ai-bug-fix-triage`](ai-bug-fix-triage.md) | Triage JIRA bugs against repository code to classify AI fixability. Use when reviewing a backlog of bugs to determine which ones an AI agent can fix. | :material-check: |
| [`/jira-activity`](jira-activity.md) | Summarize Jira ticket activity, including child tickets, to detect stale tickets in the backlog. Use when user asks to review one or more Jira tickets to determine if they are being worked on. | :material-check: |
| [`/jira-aipcc-create`](jira-aipcc-create.md) | Create AIPCC-org Jira issues in the RHAI project. Infers summary, description, type, and component from conversation context, confirms with the user before creating. Use when the user wants to file a new AIPCC Jira issue. | :material-check: |
| [`/jira-sprint-summary`](jira-sprint-summary.md) | Generate comprehensive sprint summaries by analyzing JIRA sprint data, including issue breakdown, progress metrics, and team performance insights. | :material-check: |
| [`/jira-upload-chat-log`](jira-upload-chat-log.md) | Use this skill to export and upload the current chat conversation as a markdown file attachment to a JIRA ticket for later review and documentation. | :material-check: |
| [`/jira-workitem-attach`](jira-workitem-attach.md) | Upload file attachments to Jira tickets. Verifies file exists and uploads via Jira API. Use when user wants to attach files to tickets. | :material-check: |
| [`/jira-workitem-comment`](jira-workitem-comment.md) | Add comments to Jira tickets using simple text or Jira markup (ADF JSON). Supports rich formatting with code blocks, lists, mentions, and links. Use when user wants to comment on a ticket. | :material-check: |
| [`/jira-workitem-search`](jira-workitem-search.md) | Search Jira tickets using JQL queries. Provides common query templates and flexible output formats. Use when user needs to find or filter tickets. | :material-check: |
| [`/jira-workitem-view`](jira-workitem-view.md) | Retrieve and display full details of a Jira ticket. Fetches all fields and formats them for conversation context. Use when user needs ticket information or wants to examine a ticket. | :material-check: |
| [`/pr-jira-linker`](pr-jira-linker.md) | Find and link Jira issues to PRs/MRs that are missing Jira references. Supports single PR/MR linking and batch audit of configured repos. Use when the user mentions "link PR to Jira", "scan PRs", "PR audit", "MR missing Jira", "link merge request", or wants to connect code changes to Jira for traceability. | :material-check: |
| [`/triage-bug-readiness`](triage-bug-readiness.md) | Use when assessing a Jira bug ticket for AI autofix readiness. Produces a structured JSON verdict (ready/needs_info/not_fixable) based on a three-gate rubric. Designed for CI pipeline use with the jira-triage orchestrator. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-jira@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-jira` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
