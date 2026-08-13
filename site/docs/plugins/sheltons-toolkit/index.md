---
title: sheltons-toolkit
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# sheltons-toolkit

OpenShift/RHOAI cluster-lifecycle automation (install, DSC creation, cleanup, image patching, manifest deploy, gateway/disconnected config), an AI Safety regression test runner, a multi-persona PR reviewer, and Jira hygiene checking. The cluster-lifecycle skills drive an internal Red Hat installer (olminstall) via a user-supplied OLMINSTALL_REPO_URL env var — they are usable by anyone with olminstall access, not just one team.

!!! info "Plugin Details"

    - **Version**: 1.0.0
    - **Author**: Shelton Cyril
    - **License**: MIT
    - **Scope**: Team-specific
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [sheltoncyril/sheltons-toolkit](https://github.com/sheltoncyril/sheltons-toolkit)
    - **Tags**: <span class="tag-pill">openshift</span> <span class="tag-pill">kubernetes</span> <span class="tag-pill">rhoai</span> <span class="tag-pill">cluster-lifecycle</span> <span class="tag-pill">olm</span> <span class="tag-pill">jira</span> <span class="tag-pill">pr-review</span> <span class="tag-pill">regression-testing</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/create-dsc`](create-dsc.md) | Create a DataScienceCluster (DSC) on an OpenShift cluster with RHOAI, waiting for Ready state | :material-check: |
| [`/install-operator`](install-operator.md) | Install any individual RHOAI dependency operator on an OpenShift cluster using install-operator.sh | :material-check: |
| [`/install-dependencies`](install-dependencies.md) | Install all RHOAI dependency operators via GitOps or Helm mode using setup-dependencies.sh or setup-helm.sh | :material-check: |
| [`/install-rhoai-nightly`](install-rhoai-nightly.md) | Install a RHOAI nightly build from an FBC fragment image, including cluster-type detection, pull-secret workarounds, dependency operators, and DSC creation | :material-check: |
| [`/cleanup-rhoai`](cleanup-rhoai.md) | Uninstall RHOAI operator and optionally all dependency operators/CRDs from an OpenShift cluster | :material-check: |
| [`/patch-operator-image`](patch-operator-image.md) | Patch the TrustyAI service operator deployment to use a candidate image for testing, with automatic revert | :material-check: |
| [`/deploy-component-manifests`](deploy-component-manifests.md) | Deploy custom component manifests into an OLM-deployed ODH/RHOAI operator via a kustomize overlay and PVC mount, with revert support | :material-check: |
| [`/configure-disconnected`](configure-disconnected.md) | Configure the RHCL operator for disconnected/air-gapped OpenShift environments (WASM shim patching, pull secret propagation, mirror registry) | :material-check: |
| [`/configure-gateway`](configure-gateway.md) | Configure the MaaS or llm-d inference gateway (or MaaS PostgreSQL) on an OpenShift/RHOAI cluster, in connected or disconnected mode | :material-check: |
| [`/verify-install`](verify-install.md) | Verify RHOAI installation status on an OpenShift cluster — operator CSV, DSC status, dependency operators, pod health, routes, and common issues | :material-check: |
| [`/regression-test-runner`](regression-test-runner.md) | End-to-end regression testing workflow for TrustyAI/AI Safety components — patches images, runs pytest as on-cluster Jobs, analyzes failures, creates fix PRs, and updates Jira | :material-check: |
| [`/review`](review.md) | Multi-persona PR review — spawns 3 parallel agents (chill, grumpy, unhinged) that each review from a different angle, merging findings with confidence scoring | :material-check: |
| [`/jira-hygiene-check`](jira-hygiene-check.md) | Check Jira tickets against team hygiene rules, user-scoped by default or team-wide with --team, reporting rule-ID-referenced violations | :material-check: |
| [`/jira-hygiene-setup`](jira-hygiene-setup.md) | Configure Jira Hygiene Checker with project key, team component, code repos, workflow statuses, and enforcement preferences | :material-check: |

## Installation

```bash
/plugin install sheltons-toolkit@opendatahub-skills
```
