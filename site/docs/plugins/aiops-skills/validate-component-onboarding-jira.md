---
title: validate-component-onboarding-jira
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# validate-component-onboarding-jira

Pre-flight validation tool for ODH component onboarding. Given a Jira issue
URL, fetches issue details, downloads the component_onboarding_details.yaml
attachment, and validates it against the JSON Schema. Cross-validates
repo_branch for RHOAI (must match target version), checks Dockerfile digest
pinning for RHOAI components, and updates Jira with validation results
(labels: validation-successful/validation-failed, status: In Progress).

**Plugin**: [aiops-skills](index.md) | **:material-check: User-invocable**

## Arguments

```bash
/validate-component-onboarding-jira <JIRA_URL>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `JIRA_URL` | :material-check: | - | Jira ticket URL containing the component_onboarding_details.yaml attachment to validate. |

## Usage

```bash
/validate-component-onboarding-jira https://redhat.atlassian.net/browse/RHOAIENG-12345
```
