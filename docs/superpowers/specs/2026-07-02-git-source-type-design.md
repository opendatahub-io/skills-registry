# Support non-GitHub source types (e.g. GitLab)

Closes: https://github.com/opendatahub-io/skills-registry/issues/74

## Problem

All git-based source types assume GitHub hosting. URLs like
`https://github.com/{repo}.git` and `https://raw.githubusercontent.com/...`
are hardcoded across scripts. Plugins hosted on GitLab or other forges
cannot be registered.

## Approach

Add a `git` source type with an explicit `url` field. Keep `github` as
ergonomic sugar where `repo: owner/name` implies the GitHub URL. Introduce
shared helper functions so every script resolves URLs through one place.

## Schema

The `source` definition uses conditional validation (`if`/`then`) to enforce
the right fields per type:

- **`type: github`** (existing, backwards-compatible): requires `repo`
  (owner/slug). `url` is forbidden. Optional: `ref`, `sha`, `path`.
- **`type: git`** (new): requires `url`. `repo` is forbidden.
  Optional: `ref`, `sha`, `path`.

Other types (`git-subdir`, `npm`, `local`) are unchanged.

Example `type: git` entry:

```yaml
source:
  type: git
  url: https://gitlab.corp.example.com/team/my-plugin.git
  ref: main
```

### Schema changes to `source` definition

Add `url` property:

```json
"url": {
  "type": "string",
  "format": "uri",
  "description": "Clone URL for git source type"
}
```

Add conditional validation:

```json
"allOf": [
  {
    "if": { "properties": { "type": { "const": "github" } }, "required": ["type"] },
    "then": { "required": ["repo"] }
  },
  {
    "if": { "properties": { "type": { "const": "git" } }, "required": ["type"] },
    "then": { "required": ["url"] }
  }
]
```

Change `required` on `source` from `["type", "repo"]` to `["type"]` (since
`git` type uses `url` instead of `repo`).

## Helper functions

Add to `registry_contracts.py`:

### `source_clone_url(source: dict) -> str`

- `github` -> `https://github.com/{repo}.git`
- `git` -> `source["url"]`
- Other types -> raise `ValueError`

### `source_display_name(source: dict) -> str`

For use in catalogs, site pages, and log messages.

- `github` -> `repo` as-is (e.g. `opendatahub-io/rfe-creator`)
- `git` -> strip scheme and trailing `.git` from `url`
  (e.g. `https://gitlab.corp.example.com/team/my-plugin.git`
  -> `gitlab.corp.example.com/team/my-plugin`)

### `source_browse_url(source: dict) -> str`

For constructing clickable links in markdown.

- `github` -> `https://github.com/{repo}`
- `git` -> `url` stripped of trailing `.git`

## Script changes

### `validate_registry.py`

- `check_sources()`: for `type: git`, use `git ls-remote <url>` instead of
  `gh api`. Keep `gh api` for `github`.
- `validate_remote_plugin()`: use `source_clone_url()` instead of hardcoded
  `https://github.com/{repo}.git`. Accept both `github` and `git` types
  (currently skips non-github).

### `run_skill_linter.py`

- Rename `_ensure_github_repo` -> `_ensure_repo`.
- Use `source_clone_url()` for clone URLs.
- `skill_is_skill_linter_candidate()`: accept `git` type alongside `github`.
  The gate becomes: source type is `github` or `git`, has a valid clone URL,
  and has `contract.source_assertions.skill_path`.
- `_run_one_skill()`: same generalization — remove the `github`-only gate.

### `check_versions.py`

- For `type: github`: keep existing `gh api` path (fast, no clone).
- For `type: git`: shallow clone to a `tempfile.TemporaryDirectory()`, read
  `.claude-plugin/plugin.json`, parse version, clean up. This is a weekly
  job; performance is not critical.
- Use `source_clone_url()` for the clone URL.

### `generate_catalog.py`

- `render_plugin()`: replace `https://github.com/{repo}` with
  `source_browse_url()` and `source_display_name()`.

### `generate_site.py`

- `generate_plugin_page()`: replace `https://github.com/{repo}` link with
  `source_browse_url()` / `source_display_name()`.
- `generate_llms_full_txt()`: same replacement.

### `sync_marketplace.py`

- `plugin_to_marketplace_entry()`: for `git` type, emit `url` in the
  marketplace source block instead of `repo`.

## Test changes

- Add unit tests for `source_clone_url`, `source_display_name`,
  `source_browse_url` in `test_registry_contracts.py`.
- Add `type: git` fixtures to existing test files where `type: github`
  fixtures exist.
- Test schema validation accepts `type: git` with `url`, rejects `type: git`
  without `url`, rejects `type: github` without `repo`.
- Test `check_sources` with `git ls-remote` path.
- Test `check_versions` shallow-clone path.
- Test `skill_is_skill_linter_candidate` accepts `git` type.

## Documentation changes

- `CONTRIBUTING.md`: add `type: git` example alongside the existing
  `type: github` example.
- `ARCHITECTURE.md`: update the Plugin Model section to mention the `git`
  source type.
- `CLAUDE.md`: no changes needed (it references source types generically).

## Backwards compatibility

Fully backwards-compatible. All existing `type: github` entries work
unchanged. The `repo` field keeps its current meaning for `github` sources.
No migration needed.

## Out of scope

- Adding forge-specific sugar types like `gitlab` (can be added later if
  there's demand; `type: git` with a URL covers all forges).
- `discover_skills.py` — one-time script, already run, not part of CI.
