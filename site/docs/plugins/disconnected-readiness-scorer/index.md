---
title: disconnected-readiness-scorer
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# disconnected-readiness-scorer

Score a repository's readiness for disconnected / air-gapped OpenShift deployments. Scans for image manifest completeness, digest enforcement, runtime egress, and Python dependency validation. Supports automatic detection of image management patterns (env var vs static CSV) and cross-references against the opendatahub-operator manifest.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: asanzgom
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [opendatahub-io/disconnected-readiness-scorer](https://github.com/opendatahub-io/disconnected-readiness-scorer)
    - **Tags**: <span class="tag-pill">disconnected</span> <span class="tag-pill">air-gap</span> <span class="tag-pill">openshift</span> <span class="tag-pill">image-mirroring</span> <span class="tag-pill">readiness</span> <span class="tag-pill">scoring</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/disconnected-score`](disconnected-score.md) | Score a repository's readiness for disconnected / air-gapped OpenShift deployments | :material-check: |

## Installation

```bash
/plugin install disconnected-readiness-scorer@opendatahub-skills
```
