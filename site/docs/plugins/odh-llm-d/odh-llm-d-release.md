---
title: odh-llm-d-release
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-llm-d-release

Orchestrate the opendatahub-io release for all llm-d components in one cycle. Collects upstream(llm-d) versions, auto-discovers the release tracker issue, then spawns parallel sub-agents — one per component (release branch, Konflux onboarder workflow, PR validation, approve+merge, Quay image verify, GitHub draft release) plus one KServe metadata PR sub-agent — and posts the final #Release# tracker comment. Use when the release manager runs on/before ODH code-freeze date for the llm-d team.

**Plugin**: [odh-llm-d](index.md) | **:material-check: User-invocable**

## Usage

```bash
/odh-llm-d-release
```
