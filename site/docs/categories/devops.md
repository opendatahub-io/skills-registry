---
title: DevOps & CI/CD
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# DevOps & CI/CD

Skills for deployment, CI/CD, and infrastructure

## SDLC

### [ec-cve-check](../plugins/ec-cve-check/index.md)

Inspect Enterprise Contract CVE scan results from Konflux-built container images and test ECP exception removal. Extracts the full Clair REPORTS data from cosign attestations (the same data EC's cve.cve_blockers rule evaluates), supports human-readable and JSON output, and can drive local or cluster-based EC policy validation to check whether a cve.cve_blockers exception is still needed.

**1 skills** - v0.1.0

### [disconnected-readiness-scorer](../plugins/disconnected-readiness-scorer/index.md)

Score a repository's readiness for disconnected / air-gapped OpenShift deployments. Scans for image manifest completeness, digest enforcement, runtime egress, and Python dependency validation. Supports automatic detection of image management patterns (env var vs static CSV) and cross-references against the opendatahub-operator manifest.

**1 skills** - v0.1.0

### [aiops-skills](../plugins/aiops-skills/index.md)

DevOps and TestOps automation skills for ODH/RHOAI — component onboarding, Konflux CI/CD, release management, delivery pipelines, and operational tooling.

**2 skills** - v0.1.0

### [pipeline-skills](../plugins/pipeline-skills/index.md)

Pipeline failure analysis skills for AIPCC CI/CD pipelines. Groups failed jobs by shared root cause using preprocessed error logs, then performs root cause analysis per group with structured findings, section files, and confidence-rated diagnoses. Designed to run inside a Claude Code container as part of the pipeline-failure-analyzer CI pipeline.

**2 skills** - v0.1.0
