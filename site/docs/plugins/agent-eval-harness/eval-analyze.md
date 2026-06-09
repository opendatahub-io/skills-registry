---
title: eval-analyze
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-analyze

Deep-reads a target skill and generates eval.yaml -- the configuration that
/eval-run needs. Examines the skill's SKILL.md, follows sub-skill chains
recursively (typically 2-5 levels, capped at 5 to avoid circular references)
until it finds the skills that produce the final artifacts, explores scripts
and test cases, and produces a complete config with execution mode, dataset
schema, output descriptions, judges, model defaults, and thresholds. Uses an
Explore sub-agent for the recursive skill analysis, validates the result with
validate_eval.py, and caches the analysis in eval.md with a content hash of
the top-level SKILL.md for staleness detection. The guiding principle is
"observe, don't assume" -- every field name and path must come from a file
actually read. Auto-invoked by /eval-run when eval.yaml is missing.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-analyze diagram](eval-analyze.svg)
</div>

## Arguments

```bash
/eval-analyze [--skill <name>] [--config <path>] [--update]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--skill` |  | `auto-detect` | Which skill to analyze. If omitted, lists all project skills (excluding eval harness skills) and picks automatically if only one is found. |
| `--config` |  | `auto-discover` | Output path for the eval config file. If omitted, discovers existing layout and scaffolds at the project root or eval/<skill-name>/eval.yaml. |
| `--update` |  | `false` | Fill in missing sections only, preserving user edits. Useful for upgrading older configs (e.g., adding a models block, migrating check signatures). |

## Usage

```bash
/eval-analyze --skill my-skill
/eval-analyze --update
/eval-analyze --skill rfe.create --config eval-rfe.yaml
```
