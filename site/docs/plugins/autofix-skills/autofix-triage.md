---
title: autofix-triage
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# autofix-triage

Assess a Jira bug ticket for AI autofix readiness using a three-gate
rubric. Gate 1: Can the agent start? (repo URL, clear symptom). Gate 2:
Can the agent find and fix it? (locatable code, unambiguous behavior).
Gate 3: Should an agent fix this? (not blocked by design, infrastructure,
or external deps). Produces a structured JSON verdict
(ready/needs_info/not_fixable) with confidence level. Biased toward
"ready" — a wasted autofix cycle is cheaper than a missed fix.

**Plugin**: [autofix-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![autofix-triage diagram](autofix-triage.svg)
</div>

## Usage

```bash
/autofix-triage
```
