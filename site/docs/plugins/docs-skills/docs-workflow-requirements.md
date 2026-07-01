---
title: docs-workflow-requirements
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-requirements

Analyze documentation requirements for a JIRA ticket using a two-pass fanout. Pass 1 dispatches a discovery agent to enumerate requirements. Pass 2 fans out one deep-analysis agent per requirement for isolated, thorough analysis. Assembles the standard requirements.md output. Invoked by the orchestrator.


**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Usage

```bash
/docs-workflow-requirements
```
