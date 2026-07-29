---
title: architecture-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# architecture-review

Internal forked reviewer sub-agent (context: fork, model: opus) for the
strategy workflow. Acts as a platform architect assessing refined strategy
features in artifacts/strat-tasks/ (cross-referenced against source RFEs)
for architectural correctness: verifies every dependency against the
architecture docs, checks integration patterns match how components actually
communicate, ensures component boundaries aren't violated, validates the
deployment model, and flags architectural conflicts and cross-component
coordination needs (versioning, rollout order, backwards compatibility).
Applies architecture-context overlays as authoritative corrections, skips
cleanly when no architecture context is available, and grounds every
finding in specific docs, components, or APIs.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![architecture-review diagram](architecture-review.svg)
</div>

## Usage

```bash
/architecture-review
```
