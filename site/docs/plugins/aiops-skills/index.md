---
title: aiops-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# aiops-skills

DevOps and TestOps automation skills for ODH/RHOAI — component onboarding,
Konflux CI/CD, release management, delivery pipelines, and operational tooling.

Provides an interactive onboarding pipeline for new ODH/RHOAI components:
collects component parameters through guided Q&A, generates a validated
component_onboarding_details.yaml, creates or updates Jira tickets with the
YAML attached, and validates existing onboarding tickets against a JSON Schema
with cross-checks for branch naming, Dockerfile digest pinning, and product-specific
requirements. Supports both ODH (CI and Release builds) and RHOAI (with architecture
selection, release categories, and operator manifest handling).


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [opendatahub-io/aiops-infra](https://github.com/opendatahub-io/aiops-infra)
    - **Tags**: <span class="tag-pill">devops</span> <span class="tag-pill">testops</span> <span class="tag-pill">odh</span> <span class="tag-pill">rhoai</span> <span class="tag-pill">konflux</span> <span class="tag-pill">onboarding</span> <span class="tag-pill">ci-cd</span> <span class="tag-pill">release</span> <span class="tag-pill">automation</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/create-component-onboarding-jira`](create-component-onboarding-jira.md) | Interactively collect component onboarding parameters and create/update a Jira ticket | :material-check: |
| [`/validate-component-onboarding-jira`](validate-component-onboarding-jira.md) | Pre-flight validation for ODH component onboarding — fetches Jira, downloads YAML, validates against schema | :material-check: |

## Installation

```bash
/plugin install aiops-skills@opendatahub-skills
```

## Architecture

Two skills form a create-then-validate pipeline for component onboarding:

create-component-onboarding-jira runs an 8-step interactive flow: parse input,
check prerequisites (uv, jq, Jira credentials), collect parameters via guided
Q&A with product-aware conditional logic (ODH vs RHOAI), generate YAML, validate
against JSON Schema, create or update a Jira ticket (cloning product-specific
templates if no URL provided), attach the YAML, and report results.

validate-component-onboarding-jira runs a 6-step validation flow: check
prerequisites, create working directory from Jira URL, fetch issue details,
download YAML attachment, validate against schema with cross-checks (branch
naming for RHOAI, Dockerfile digest pinning), and update Jira with
validation-successful or validation-failed labels.

Both skills use deterministic Python scripts (run via uv) for Jira API
operations and YAML schema validation. The component_onboarding_details.schema.json
defines conditional requirements based on product_context (ODH vs RHOAI) and
is_operator fields.
