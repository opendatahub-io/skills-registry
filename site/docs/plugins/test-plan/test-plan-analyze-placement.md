---
title: test-plan-analyze-placement
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-analyze-placement

Internal forked sub-agent for test case placement analysis. Classifies each TC
by test level (unit, integration, k8s-integration, api, e2e) and scores placement
options (same_repo, downstream, both) using factors: test level preferences,
infrastructure requirements, TC priority (P0 prefers upstream for fast feedback),
and code repo agent readiness. Returns recommendations with user confirmation.

**Plugin**: [test-plan](index.md) | **:material-close: Internal**

## Diagram

<div class="diagram-container" markdown>
![test-plan-analyze-placement diagram](test-plan-analyze-placement.svg)
</div>

## Usage

```bash
/test-plan-analyze-placement
```
