---
title: konflux-build-simulator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# konflux-build-simulator

Analyzes a repository and generates GitHub Actions workflows that simulate
the Konflux build environment at PR time, catching failures before they
reach production. Performs validation across six phases: static checks
(hermetic lockfiles, workspace dependencies, FIPS compliance), Docker build
validation, runtime validation (crashloop detection, API endpoint testing,
WebSocket compatibility), module federation validation (remoteEntry.js,
chunk integrity, load performance), operator integration (Kind cluster),
and manifest validation (kustomize, ConfigMap, overlays).

Automatically detects repository type (monorepo, Kubernetes operator, or
component/library) and generates appropriate validation phases. Key
RHOAI-specific checks include Hermeto/Cachi2 hermetic build compatibility,
FIPS strictfipsruntime enforcement, and fastify v5 regression testing.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![konflux-build-simulator diagram](konflux-build-simulator.svg)
</div>

## Arguments

```bash
/konflux-build-simulator [repository-url]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository-url` |  | - | GitHub repository URL to generate build simulation for (prompted if omitted) |

## Usage

```bash
/konflux-build-simulator https://github.com/opendatahub-io/odh-dashboard
/konflux-build-simulator https://github.com/opendatahub-io/kserve
/konflux-build-simulator https://github.com/kubeflow/training-operator
```
