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
 │  rfe-creator ├───────►│ opendatahub-io/rfe-creator     │
 │              │        │  └─ .claude/skills/            │
 │              │        │      ├─ rfe.create/SKILL.md    │
 │              │        │      ├─ rfe.review/SKILL.md    │
 │              │        │      └─ ...                    │
 │              │        └────────────────────────────────┘
 │              │
 │              │        ┌────────────────────────────────┐
 │  assess-rfe  ├───────►│ opendatahub-io/assess-rfe      │
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

### Source Types

- **`type: github`** — shorthand for GitHub repos. Only requires `repo: owner/name`;
  clone and browse URLs are derived automatically.
- **`type: git`** — explicit clone URL for any git forge (GitLab, Gitea, Bitbucket, etc.).
  Requires `url` (the clone URL). Browse links strip the trailing `.git` suffix.
- **`type: git-subdir`** — subdirectory within a git repo (uses `path`).
- **`type: npm`** / **`type: local`** — non-git source types.

### Dependencies

Plugins can declare `depends_on: [other-plugin]` to express inter-plugin
dependencies within the registry. This is registry-level metadata only —
it is not propagated to `marketplace.json` (Claude Code does not support
registry-level dependency resolution).

### Meta-plugins (bundles)

A **meta-plugin** (bundle) is a plugin that installs a set of other plugins in
one step. It lists its members with `includes`:

```yaml
  - name: patternfly            # the bundle — no skills of its own
    includes: [pf-react, pf-a11y, pf-mcp]   # names of member plugins
  - name: pf-react              # a member, registered as its own entry
    skill_count: 10
    source: { type: git-subdir, url: ..., path: plugins/patternfly/pf-react }
```

- **Members must be registered as their own top-level entries** in this
  registry, with names matching the bundle's upstream `plugin.json`
  `dependencies`. Claude Code resolves a plugin's dependencies *within the same
  marketplace it was installed from*, so a bundle whose members are absent from
  this registry would install with zero skills (`dependency-unsatisfied`).
- The bundle's displayed skill count is **derived** by summing its members'
  counts (single source of truth), and bundles are **excluded from
  registry-wide totals** so each skill is counted exactly once.
- `includes` is distinct from `depends_on`: `depends_on` records a required
  peer plugin; `includes` means "installing this installs these" and drives the
  catalog/site **Includes** section. Neither is propagated to `marketplace.json`.
- `validate_registry.py` (`check_bundles`) enforces that members are defined,
  a bundle neither lists itself nor forms a cycle, and a bundle carries no
  `skills`/`skill_count` of its own.

### Delegated skill discovery (`skill_count`)

A plugin that delegates skill discovery to its own `plugin.json` (e.g. a
`git-subdir` sub-plugin) carries no `skills` array in `registry.yaml`, so the
catalog would otherwise show "0 skills". Set `skill_count: N` to record the
number for display. It is catalog-only metadata (not propagated to
`marketplace.json`); the actual skills are still discovered from the source
repo at install time. A plugin may set `skill_count` **or** list `skills`, not
both.

### Agents and MCP servers

Besides skills, a plugin may provide **agents** (`agents` + `agents_dir`) and
**MCP servers** (`mcp_servers`). Each renders as its own table on the plugin's
catalog and site page. `agents_dir` (like `skills_dir`) points the marketplace
entry at agent files for `strict: false` plugins. `mcp_servers` is catalog-only
display metadata (name + description of each server declared in the source
`plugin.json` `mcpServers`); Claude Code reads the real config from that
`plugin.json`, so it is never propagated to `marketplace.json`. This lets an
MCP-only plugin (e.g. `pf-mcp`) advertise what it provides instead of reading as
"0 skills".

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
