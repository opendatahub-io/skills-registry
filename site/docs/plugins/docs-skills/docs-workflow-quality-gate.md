---
title: docs-workflow-quality-gate
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-workflow-quality-gate

Score documentation quality and intent alignment using LLM judge agents (Opus). Dispatches two judge agents in parallel (doc_quality, intent_alignment), extracts specific gaps from AC coverage analysis, and cross-references against scope-req-audit evidence. Produces pass/fail gate with actionable gap list. Iteration logic is owned by the orchestrator, not this skill.


**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Usage

```bash
/docs-workflow-quality-gate
```
