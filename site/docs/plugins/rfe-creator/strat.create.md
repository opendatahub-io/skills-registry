---
title: strat.create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strat.create

Create strategies from approved RFEs by cloning them to the RHAISTRAT
project in Jira. Supports both Atlassian MCP and REST API fallback for
reading RFE data. When Jira MCP is available, clones issues directly;
otherwise generates a manual cloning guide. Creates local strategy stub
files in artifacts/strat-tasks/ with the business need copied from the
source RFE, ready for refinement with strat.refine.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![strat.create diagram](strat.create.svg)
</div>

## Usage

```bash
/strat.create RHAIRFE-1234
/strat.create
```
