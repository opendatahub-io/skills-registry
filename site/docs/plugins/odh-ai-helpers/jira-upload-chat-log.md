---
title: jira-upload-chat-log
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# jira-upload-chat-log

Export the current chat conversation as a formatted markdown document
(with both a summary and full transcript) and upload it as a file
attachment to a Jira ticket. Automatically detects ticket keys from
conversation context, or prompts the user if none is found. Delegates
the actual upload to the jira-workitem-attach skill.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![jira-upload-chat-log diagram](jira-upload-chat-log.svg)
</div>

## Arguments

```bash
/jira-upload-chat-log [TICKET_KEY]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `TICKET_KEY` |  | `auto-detected from conversation context` | Jira ticket key (e.g., AIPCC-1234) |

## Usage

```bash
/jira-upload-chat-log AIPCC-7354
/jira-upload-chat-log
```
