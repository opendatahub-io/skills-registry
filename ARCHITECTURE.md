# Architecture

## Overview

The skills-registry is a centralized catalog that aggregates Claude Code plugins
from multiple GitHub repositories into a single discoverable marketplace. It acts
as an indirection layer: plugin source code lives in separate repos, while this
registry provides the metadata and discovery mechanism.

Plugins in this registry conform to the [Agent Skills](https://agentskills.io/specification)
open standard, extended by Claude Code with features like invocation control
and subagent execution (see [Claude Code skills](https://code.claude.com/docs/en/skills)).

```
                        skills-registry
┌──────────────────────────────────────────────────────┐
│                                                      │
│  registry.yaml          (source of truth)            │
│       │                                              │
│       ├──► marketplace.json   (Claude Code native)   │
│       ├──► catalog.md         (human-readable)       │
│       │                                              │
│  schema/                (validation)                 │
│  scripts/               (automation)                 │
│  .github/workflows/     (CI)                         │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Data Flow

```
                 ┌─────────────────┐
                 │  registry.yaml  │  Single source of truth
                 │                 │  (edited by humans)
                 └────────┬────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
     sync_marketplace  generate    validate
          .py          _catalog     _registry
                        .py          .py
              │           │           │
              ▼           ▼           ▼
     marketplace.json  catalog.md   pass/fail
     (Claude Code)     (docs)       (CI gate)
```

## File Structure

```
skills-registry/
├── registry.yaml                    # Source of truth
├── .claude-plugin/
│   └── marketplace.json             # Generated — Claude Code reads this
├── catalog.md                       # Generated — human-readable listing
├── schema/
│   └── registry.schema.json         # JSON Schema for registry.yaml
├── scripts/
│   ├── validate_registry.py         # Schema + structure validation
│   ├── sync_marketplace.py          # registry.yaml -> marketplace.json
│   ├── generate_catalog.py          # registry.yaml -> catalog.md
│   └── check_versions.py            # Poll plugin repos for version bumps
├── .github/workflows/
│   └── validate.yml                 # CI: validate + sync check
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## Plugin Model

Each plugin entry in `registry.yaml` points to an external GitHub repo
that contains the actual skills:

```
  registry.yaml                     External Repos
 ┌──────────────┐
 │ plugins:     │
 │              │        ┌────────────────────────────────┐
 │  rfe-creator ├───────►│ jwforres/rfe-creator           │
 │              │        │  └─ .claude/skills/            │
 │              │        │      ├─ rfe.create/SKILL.md    │
 │              │        │      ├─ rfe.review/SKILL.md    │
 │              │        │      └─ ...                    │
 │              │        └────────────────────────────────┘
 │              │
 │              │        ┌────────────────────────────────┐
 │  assess-rfe  ├───────►│ n1hility/assess-rfe            │
 │  (strict:    │        │  ├─ .claude-plugin/            │
 │   true)      │        │  │   └─ plugin.json            │
 │              │        │  └─ skills/                    │
 │              │        │      ├─ assess-rfe/SKILL.md    │
 │              │        │      └─ export-rubric/SKILL.md │
 │              │        └────────────────────────────────┘
 └──────────────┘
```

### Strict vs Non-Strict Plugins

- **strict: true** (default) — `plugin.json` in the repo is the authority
  for component definitions. The marketplace entry can supplement it with
  additional components, and both sources are merged. Use this for repos
  that have their own `.claude-plugin/plugin.json`.

- **strict: false** — The marketplace entry is the entire plugin definition.
  If the repo also has a `plugin.json` that declares components, that is a
  conflict and the plugin fails to load. Use `skills_dir` to tell Claude
  Code where to find skills in the repo. **Required for repos without a
  `plugin.json`** — without it, Claude Code has no way to discover skills
  when installing via a marketplace.

Note: `skills_dir` must not be specified without `strict: false`. The schema
and validation scripts enforce this constraint.

### Dependencies

Plugins can declare `depends_on: [other-plugin]` to express inter-plugin
dependencies within the registry. This is registry-level metadata only —
it is not propagated to `marketplace.json` (Claude Code does not support
dependency resolution).

## CI Pipeline

```
  push/PR to main
        │
        ▼
  ┌─────────────────────────────┐
  │  validate.yml               │
  │                             │
  │  1. validate_registry.py    │  Schema validation
  │       │                     │
  │  2. sync_marketplace.py     │  Regenerate marketplace.json
  │       │                     │
  │  3. git diff --exit-code    │  Fail if marketplace.json
  │     marketplace.json        │  is out of sync
  │       │                     │
  │  4. generate_catalog.py     │  Regenerate catalog.md
  │       │                     │
  │  5. git diff --exit-code    │  Fail if catalog.md
  │     catalog.md              │  is out of sync
  └─────────────────────────────┘
```

CI does **not** auto-commit — it only verifies that the generated files
match the registry. Contributors must run the scripts locally before pushing.

## How Claude Code Discovers Plugins

```
  Developer                     Claude Code                 GitHub
     │                              │                          │
     │  claude plugin marketplace   │                          │
     │  add opendatahub-io/         │                          │
     │      skills-registry         │                          │
     │─────────────────────────────►│                          │
     │                              │  fetch marketplace.json  │
     │                              │─────────────────────────►│
     │                              │◄─────────────────────────│
     │                              │                          │
     │  /plugin install             │                          │
     │  rfe-creator@opendatahub-    │                          │
     │  skills                      │                          │
     │─────────────────────────────►│  clone source repo       │
     │                              │─────────────────────────►│
     │                              │◄─────────────────────────│
     │                              │                          │
     │  /rfe.create                 │                          │
     │─────────────────────────────►│  (runs skill locally)    │
     │◄─────────────────────────────│                          │
```

## Adding a New Plugin

1. Add an entry to `registry.yaml`
2. Run `python3 scripts/validate_registry.py`
3. Run `python3 scripts/sync_marketplace.py`
4. Run `python3 scripts/generate_catalog.py`
5. Commit all changes and open a PR
6. CI verifies everything is in sync

## References

- [Agent Skills specification](https://agentskills.io/specification) — open standard for skill definitions
- [Claude Code skills](https://code.claude.com/docs/en/skills) — SKILL.md frontmatter and invocation semantics
- [Claude Code sub-agents](https://code.claude.com/docs/en/sub-agents) — agent frontmatter and delegation
- [Claude Code plugins](https://code.claude.com/docs/en/plugins) — plugin manifest and marketplace format
