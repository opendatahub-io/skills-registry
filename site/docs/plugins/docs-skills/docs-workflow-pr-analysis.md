---
title: docs-workflow-pr-analysis
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-pr-analysis

Run PR/MR analysis for the docs orchestrator workflow. Dispatches a subagent to run understand-pull-request, keeping the heavy orchestration out of the main context. Produces a structured PR-ANALYSIS.md. Conditional on has_pr — skipped when no PR URL is available.


**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Usage

```bash
/docs-workflow-pr-analysis
```
