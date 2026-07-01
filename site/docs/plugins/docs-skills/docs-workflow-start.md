---
title: docs-workflow-start
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-start

Interactive guided setup for the docs workflow. Only invoke this skill when the user explicitly requests docs-workflow-start (e.g., /docs-workflow-start). Do NOT invoke this skill when the user requests docs-orchestrator — that skill runs directly. When invoked with no CLI switches, uses AskUserQuestion to gather configuration. Supports full workflow, individual steps with auto-resolved prerequisites, and resuming previous runs. When switches are provided, passes through directly to docs-orchestrator.


**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Usage

```bash
/docs-workflow-start
```
