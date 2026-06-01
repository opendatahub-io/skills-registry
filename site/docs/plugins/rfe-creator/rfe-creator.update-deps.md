---
title: rfe-creator.update-deps
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-creator.update-deps

Force update all vendored dependencies by removing cached copies and
re-fetching. Updates the assess-rfe skills (from the assess-rfe plugin)
and architecture context (from opendatahub-io/architecture-context).
Has disable-model-invocation set, meaning it can only be triggered
explicitly by the user.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe-creator.update-deps diagram](rfe-creator.update-deps.svg)
</div>

## Usage

```bash
/rfe-creator.update-deps
```
