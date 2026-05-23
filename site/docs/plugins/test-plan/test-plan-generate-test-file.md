---
title: test-plan-generate-test-file
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-generate-test-file

Internal forked sub-agent for parallel test file generation. Receives test case
data, repository conventions, and pattern guides. Generates complete test files
with framework-appropriate structure (imports, fixtures, AAA pattern functions),
validates syntax, scores quality via test-plan-score-test-function, and auto-revises
low-scoring functions. Returns result via temp file for parent to write.

**Plugin**: [test-plan](index.md) | **:material-close: Internal**

## Diagram

<div class="diagram-container" markdown>
![test-plan-generate-test-file diagram](test-plan-generate-test-file.svg)
</div>

## Usage

```bash
/test-plan-generate-test-file
```
