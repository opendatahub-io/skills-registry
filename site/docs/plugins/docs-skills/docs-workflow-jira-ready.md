---
title: docs-workflow-jira-ready
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-jira-ready

Check whether a JIRA query returns tickets ready for the docs workflow. Queries JIRA via jira_reader.py, filters out tickets that already have a workflow progress file or a "docs-workflow-started" label, and outputs a JSON list of actionable ticket IDs. Designed as the entry point for cron-triggered or CI-triggered docs-orchestrator runs.


**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Usage

```bash
/docs-workflow-jira-ready
```
