---
title: jira-reader
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# jira-reader

Read-only access to JIRA issues on the Red Hat Issue Tracker via the
Atlassian REST API v3 (auto-converting Atlassian Document Format to plain
text). Fetches full issue details, searches by JQL (fast summary mode by
default, or `--fetch-details` for full fields), extracts comments (with
anonymized participants) and custom fields (release-note type, fix versions),
finds linked Git PRs/commits, categorizes issues, and traverses the ticket
graph (`--graph`: ancestors, children, siblings, issue links, web links).
Respects JIRA rate limits. Auth via `JIRA_API_TOKEN` + `JIRA_EMAIL`; PEP 723
script (jira, ratelimit).

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![jira-reader diagram](jira-reader.svg)
</div>

## Arguments

```bash
/jira-reader --issue <KEY>... | --jql <query> [--fetch-details] | --graph <KEY> [--max-children N] [--max-siblings N] [--max-links N] [--include-comments]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--issue` |  | - | Fetch full details for one or more issues. Repeatable. |
| `--jql` |  | - | Search issues by JQL (summary mode; add --fetch-details for full fields). |
| `--graph` |  | - | Traverse the ticket relationship graph (ancestors, children, siblings, links). |
| `--include-comments` |  | `false` | Include comment threads with --issue. |

## Usage

```bash
jira_reader.py --issue INFERENG-5233 --include-comments
jira_reader.py --jql "project=INFERENG AND status='In Progress'"
jira_reader.py --graph INFERENG-5233
```
