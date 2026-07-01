---
title: docs-workflow-planning
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-planning

Orchestrator step that turns the requirements analysis into a documentation
plan by dispatching the `docs-planner` subagent. The plan includes gap
analysis, module specifications (type, title, audience, content points,
prerequisites, dependencies), implementation order, assembly structure, and
content sources. When code analysis is available, the planner is required to
scope modules by the registry's `onboarding_priority` (read-first → full
spec, read-second → summary, skip → no spec); when PR analysis is available
it prioritizes changed modules. Writes plan.md and a sidecar with the module
count (the orchestrator stops the pipeline if the plan has 0 modules).

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-workflow-planning diagram](docs-workflow-planning.svg)
</div>

## Arguments

```bash
/docs-workflow-planning <ticket> --base-path <path>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ticket` | :material-check: | - | JIRA ticket ID. |
| `--base-path` | :material-check: | - | Workflow base path (reads requirements/requirements.md). |

## Usage

```bash
/docs-workflow-planning PROJ-123 --base-path .agent_workspace/proj-123
```
