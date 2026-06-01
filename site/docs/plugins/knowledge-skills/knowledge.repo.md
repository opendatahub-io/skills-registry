---
title: knowledge.repo
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# knowledge.repo

Scan merged PRs from the last N days, extract knowledge relevant to AI
agent context, and propose updates to context files (CLAUDE.md, AGENTS.md)
as a git-apply-able patch. Runs a 7-phase pipeline: setup (forge detection,
context file discovery), fetch (PR data via CLI), extract (parallel haiku
agents per PR), synthesize (opus agent merges findings into proposed edits),
review (adversarial opus agent checks quality), revise (conditional fix pass),
and artifacts (patch file, run report). Non-interactive — designed for CI.

**Plugin**: [knowledge-skills](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![knowledge.repo diagram](knowledge.repo.svg)
</div>

## Arguments

```bash
/knowledge.repo [--days N]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--days` |  | `7` | How far back to scan merged PRs |

## Usage

```bash
/knowledge.repo
/knowledge.repo --days 14
/knowledge.repo --days 30
```
