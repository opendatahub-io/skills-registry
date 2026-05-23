---
title: vllm-compare-reqs
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-compare-reqs

Compare Python requirements files and Dockerfiles between vLLM versions
to identify dependency changes. Supports variant-based comparison (rocm,
cuda, cpu, tpu, xpu) which auto-includes runtime, build, and Dockerfile
differences, or single-file comparison. Produces a categorized summary
table followed by detailed per-file change listings. Designed for AIPCC
package onboarding workflows.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-compare-reqs diagram](vllm-compare-reqs.svg)
</div>

## Arguments

```bash
/vllm-compare-reqs <VERSION1> <VERSION2> <VARIANT_OR_FILE> [--pretty]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `VERSION1` | :material-check: | - | First version to compare (e.g., v0.13.0) |
| `VERSION2` | :material-check: | - | Second version to compare (e.g., v0.14.0) |
| `VARIANT_OR_FILE` | :material-check: | - | Variant name (rocm, cuda, cpu, tpu, xpu) or specific file (common.txt, rocm-build.txt) |
| `--pretty` |  | `true` | Show clean categorized output (use --no-pretty for simple diff) |

## Usage

```bash
/vllm-compare-reqs v0.13.0 v0.14.0 rocm
/vllm-compare-reqs v0.13.0 v0.14.0 cuda
/vllm-compare-reqs v0.13.0 v0.14.0 common.txt
```
