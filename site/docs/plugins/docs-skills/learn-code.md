---
title: learn-code
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# learn-code

A single-skill codebase-analysis pipeline that produces an ONBOARDING.md
guide for engineer onboarding. It detects the primary language, builds a
module map, dispatches a `repo-mapper` agent to produce a per-module registry
with tailored questions, then fans out `module-analyzer` agents (in batches
of 10) with size-aware tiering — full source, API-guided (truncated source +
AST-extracted public API), or API-only (no agent). It analyzes prioritized
cross-module dependency pairs via `relationship-analyzer` agents, and a
`synthesis-writer` agent assembles the final guide from a size-bounded
context. Progress is checkpointed for resume. Accepts a local path or a git
URL (cloned automatically).

**Plugin**: [docs-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![learn-code diagram](learn-code.svg)
</div>

## Arguments

```bash
/learn-code <repo-path-or-url> [--exclude <glob>...]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repo` | :material-check: | - | Local path or git URL of the repository to analyze (URLs are cloned). |
| `--exclude` |  | - | Glob pattern(s) to exclude from analysis. Repeatable. |

## Usage

```bash
/learn-code /path/to/repo
/learn-code https://github.com/user/repo
/learn-code /path/to/repo --exclude "test/*" "vendor/*"
```
