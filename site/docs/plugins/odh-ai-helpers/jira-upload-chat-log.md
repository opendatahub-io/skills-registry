---
title: jira-upload-chat-log
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# jira-upload-chat-log

Export the current chat conversation as a markdown file and attach
it to a Jira ticket.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![jira-upload-chat-log diagram](jira-upload-chat-log.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket_key` |  | `auto-detected from conversation` | Jira ticket key (e.g., AIPCC-1234) |

## Usage

```
/jira-upload-chat-log AIPCC-7354
/jira-upload-chat-log
```
