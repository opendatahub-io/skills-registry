---
title: autofix-resolve
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# autofix-resolve

Orchestrate end-to-end bug fixing by dispatching implement and review
prompt agents in a loop. Uses state.py for persistence across context
compression. Supports resolve mode (fresh ticket) and iterate mode
(address MR/PR feedback). Extension skills called at post-implement
and post-review hook points. Hard cap of 3 implement invocations.
Never writes code directly — all coding happens through prompt agents.

**Plugin**: [autofix-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![autofix-resolve diagram](autofix-resolve.svg)
</div>

## Arguments

```bash
/autofix-resolve [mode]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `mode` |  | `resolve` | resolve = fresh ticket fix; iterate = address MR/PR feedback |

## Usage

```bash
/autofix-resolve
/autofix-resolve iterate
```
