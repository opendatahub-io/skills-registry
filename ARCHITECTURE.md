# Architecture

## Overview

The skills-registry is a centralized catalog that aggregates Claude Code plugins
from multiple GitHub repositories into a single discoverable marketplace. It acts
as an indirection layer: plugin source code lives in separate repos, while this
registry provides the metadata and discovery mechanism.

Plugins in this registry conform to the [Agent Skills](https://agentskills.io/specification)
open standard, extended by Claude Code with features like invocation control
and subagent execution (see [Claude Code skills](https://code.claude.com/docs/en/skills)).
The same standard underpins OpenAI Codex, so the one `registry.yaml` is projected
into a native marketplace for each supported harness — Claude Code
(`.claude-plugin/marketplace.json`) and OpenAI Codex
(`.agents/plugins/marketplace.json`); see [Harness Projections](#harness-projections).

```
                        skills-registry
┌──────────────────────────────────────────────────────┐
│                                                      │
│  registry.yaml          (source of truth)            │
│       │                                              │
│       ├──► marketplace.json   (Claude Code native)   │
│       ├──► .agents/plugins   (OpenAI Codex native)   │
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

`sync_codex_marketplace.py` runs the same way, projecting `registry.yaml` into
OpenAI Codex's native `.agents/plugins/marketplace.json` (see
[Harness Projections](#harness-projections)).

## File Structure

```
skills-registry/
├── registry.yaml                    # Source of truth
├── .claude-plugin/
│   └── marketplace.json             # Generated — Claude Code reads this
├── .agents/plugins/
│   └── marketplace.json             # Generated — OpenAI Codex reads this
├── catalog.md                       # Generated — human-readable listing
├── schema/
│   └── registry.schema.json         # JSON Schema for registry.yaml
├── scripts/
│   ├── validate_registry.py         # Schema + structure validation
│   ├── sync_marketplace.py          # registry.yaml -> marketplace.json
│   ├── sync_codex_marketplace.py    # registry.yaml -> .agents/plugins/marketplace.json
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

### Delegated sub-plugins and the contract exemption

A sub-plugin that delegates skill discovery to its own `plugin.json` (e.g. a
`git-subdir` bundle member) can **list its skills** (name + description) in
`registry.yaml` so they render on its catalog/site page. Such skills do **not**
require a `contract` block: the canonical-contract requirement is enforced only
for skills whose plugin `source.type` is `github`/`git` (`GIT_CLONE_TYPES`) —
the same cloneable sources `skill-linter` and the skill-name-drift check
verify. A `git-subdir`/`npm`/`local` source cannot be cloned and its
`source_assertions` cannot be resolved, so a contract on it would be
unverifiable; the exemption keeps enforcement aligned with what can actually be
verified rather than weakening it.

When only a count is wanted (no list), set `skill_count: N` instead — catalog-only
metadata (not propagated to `marketplace.json`). A plugin sets `skill_count`
**or** lists `skills`, not both. Either way the actual skills are discovered
from the source repo at install time.

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

## Harness Projections

`registry.yaml` is projected into a **native marketplace per harness**, each in
that harness's own format, from the same single source of truth:

| Harness | Generated file | Generator | Entry shape |
|---------|----------------|-----------|-------------|
| Claude Code | `.claude-plugin/marketplace.json` | `sync_marketplace.py` | `source: github` + `repo`; per-entry `skills`/`strict`/`agents` supported |
| OpenAI Codex | `.agents/plugins/marketplace.json` | `sync_codex_marketplace.py` | exactly `{name, source, policy, category}`; `github` → `source: url` clone URL; skills come from each plugin's own manifest |

Codex ([developers.openai.com/codex/plugins](https://developers.openai.com/codex/plugins/build))
reads `$REPO_ROOT/.agents/plugins/marketplace.json` (and still falls back to the
legacy `$REPO_ROOT/.claude-plugin/marketplace.json`). Key differences the Codex
projection applies:

- Top level is `{name, interface?, plugins[]}` — no `owner`/`metadata`.
  `interface.displayName` comes from the optional top-level `display_name` and is
  omitted when unset. Plugin array order is the Codex render order.
- Each entry carries a `policy` (`installation: AVAILABLE`,
  `authentication: ON_INSTALL`) and a display-name `category`
  (`categories[<key>].name`), both of which Codex asks you to always include.
- `github`/`git` sources become `{source: url, url: <clone URL>}` (Codex has no
  in-file `github`+`repo` shorthand); `git-subdir` carries a `./`-prefixed
  `path`; `ref`/`sha` carry through.

Because a Codex marketplace entry has **no per-entry `skills` array**, Codex
discovers a plugin's skills from that plugin's own `.codex-plugin/plugin.json`
manifest (its `skills` path). A `strict: false` plugin that ships no manifest in
its repo therefore installs with **zero skills under Codex** until a
`.codex-plugin/plugin.json` with a `skills` path is added upstream — the one
case where the registry-only projection is insufficient for Codex.

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
4. Run `python3 scripts/sync_codex_marketplace.py`
5. Run `python3 scripts/generate_catalog.py`
6. Run `python3 scripts/generate_site.py`
7. Commit all changes and open a PR
8. CI verifies everything is in sync

## References

- [Agent Skills specification](https://agentskills.io/specification) — open standard for skill definitions
- [Claude Code skills](https://code.claude.com/docs/en/skills) — SKILL.md frontmatter and invocation semantics
- [Claude Code sub-agents](https://code.claude.com/docs/en/sub-agents) — agent frontmatter and delegation
- [Claude Code plugins](https://code.claude.com/docs/en/plugins) — plugin manifest and marketplace format
- [OpenAI Codex plugins](https://developers.openai.com/codex/plugins/build) — Codex plugin manifest and marketplace format
