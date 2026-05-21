---
title: test-plan-analyze-infra
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-analyze-infra

Internal forked sub-analyzer. Identifies cluster configuration requirements
(OpenShift/RHOAI versions, databases, runtimes), test data requirements, test
users (service accounts, RBAC roles), infrastructure dependencies, configuration
(env vars, ConfigMaps, feature gates), and test tooling. Produces findings for
Sections 3 and 9.

**Plugin**: [test-plan](index.md) | **:material-close: Internal**

## Diagram

<div class="diagram-container" markdown>
![test-plan-analyze-infra diagram](test-plan-analyze-infra.svg)
</div>

## Usage

```bash
/test-plan-analyze-infra
```
