---
title: docs-workflow-create-jira
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-create-jira

Orchestrator step that creates a linked JIRA ticket for documentation work.
Unlike most step skills it dispatches no agent — it runs
`create-jira-ticket.sh` directly, which checks for an existing "Document"
link, probes project visibility (public vs private), extracts the JTBD
sections from the plan, converts Markdown to JIRA wiki markup, creates the
ticket with a `[ccs] Docs -` prefix, links it to the parent, and (for private
projects) attaches the plan. Writes a sidecar recording the new JIRA key/URL
or that an existing linked ticket was found.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-create-jira diagram](docs-workflow-create-jira.svg)
</div>

## Arguments

```bash
/docs-workflow-create-jira <ticket> --base-path <path> --project <PROJECT>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | Parent JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads planning/plan.md). |
| `--project` | :material-check: | - | Target JIRA project key for the new documentation ticket. |

## Usage

```bash
/docs-workflow-create-jira PROJ-123 --base-path .agent_workspace/proj-123 --project DOCS
```
