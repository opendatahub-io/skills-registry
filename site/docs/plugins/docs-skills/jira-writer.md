---
title: jira-writer
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# jira-writer

Write access to JIRA issues on the Red Hat Issue Tracker. Pushes release
notes (from a string or file), updates release-note status, modifies any
custom field, and adds/removes/swaps labels — with batch updates across
multiple issues. Performs write operations and prompts for approval before
changing anything (no allowed-tools restriction). Respects JIRA rate limits.
Auth via `JIRA_API_TOKEN` + `JIRA_EMAIL`; PEP 723 script (jira, ratelimit).
Use only when explicitly asked to modify JIRA.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![jira-writer diagram](jira-writer.svg)
</div>

## Arguments

```bash
/jira-writer --issue <KEY>... [--release-note <text> | --release-note-file <path>] [--status <val>] [--custom-field <id> --value <val>] [--labels-add <l>] [--labels-remove <l>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--issue` | :material-check: | - | Target issue key(s). Repeatable for batch updates. |
| `--release-note / --release-note-file` |  | - | Set the release-note text from a string or a file. |
| `--status` |  | - | Set the release-note status (e.g., Proposed, Approved). |
| `--custom-field / --value` |  | - | Set an arbitrary custom field to a value. |
| `--labels-add / --labels-remove` |  | - | Add or remove labels (combine to swap in one API call). |

## Usage

```bash
jira_writer.py --issue INFERENG-5233 --release-note "Fixed issue with..."
jira_writer.py --issue PROJ-123 --labels-remove docs-ready --labels-add docs-in-progress
```
