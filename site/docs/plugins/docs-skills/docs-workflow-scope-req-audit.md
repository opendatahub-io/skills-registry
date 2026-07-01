---
title: docs-workflow-scope-req-audit
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-scope-req-audit

Classify JIRA requirements by code evidence status before planning. Uses learn-code analysis data and source code inspection to determine if each requirement is grounded, partial, or absent. Fans out one subagent per requirement for isolated classification. Prevents hallucinated documentation for unimplemented features and surfaces gaps for implemented ones. Conditional on has_source_repo.


**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Usage

```bash
/docs-workflow-scope-req-audit
```
