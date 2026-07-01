---
title: docs-review-modular-docs
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-review-modular-docs

Reviews AsciiDoc (`.adoc`) files for Red Hat modular documentation
compliance: module type (concept / procedure / reference / assembly),
required sections, anchor IDs with `_{context}`, sentence-case titles,
allowed admonition types, `leveloffset` on includes, single-step-procedure
bullets, and attribute definition validation (`{product-name}` etc.). Ships
a common-violations table and consults the shared `asciidoc-reference.md`.
Applies to `.adoc` only; composed by `docs-review-style` and the AsciiDoc
style-review step.

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![docs-review-modular-docs diagram](docs-review-modular-docs.svg)
</div>

## Usage

```bash
Review this procedure module for modular docs compliance
Check if this assembly follows Red Hat modular guidelines
```
