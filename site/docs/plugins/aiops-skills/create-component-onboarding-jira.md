---
title: create-component-onboarding-jira
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# create-component-onboarding-jira

Interactively collects ODH/RHOAI component onboarding parameters from the
user, generates a validated component_onboarding_details.yaml, and creates
or updates a Jira ticket with the YAML attached. When no Jira URL is provided,
automatically creates a new ticket by cloning the product-specific onboarding
template. Supports both ODH (CI and Release builds) and RHOAI (with
architecture selection, release categories, and operator manifest handling).

**Plugin**: [aiops-skills](index.md) | **:material-check: User-invocable**

## Arguments

```bash
/create-component-onboarding-jira [JIRA_URL]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `JIRA_URL` |  | - | Existing Jira ticket URL to update. If omitted, creates a new ticket by cloning the onboarding template. |

## Usage

```bash
/create-component-onboarding-jira
/create-component-onboarding-jira https://redhat.atlassian.net/browse/RHOAIENG-12345
```
