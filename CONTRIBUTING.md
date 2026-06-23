# Contributing to the Skills Registry

## Adding a New Plugin

### 1. Prepare Your Repository

Your plugin repo needs at minimum:

**Option A — Full plugin (recommended):**
```text
your-repo/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
└── skills/                  # Or .claude/skills/
    └── your-skill/
        └── SKILL.md         # Skill definition
```

The `plugin.json` needs at least:
```json
{
  "name": "your-plugin",
  "description": "What your plugin does",
  "version": "1.0.0"
}
```

**Option B — Skills-only repo (no plugin.json):**

If your repo only has `.claude/skills/` and you can't add a `plugin.json`, you can use `strict: false` in the registry entry (see step 2).

### 2. Add Your Entry to registry.yaml

Open a PR adding your plugin to the `plugins` list in `registry.yaml`:

```yaml
plugins:
  # ... existing plugins ...

  - name: your-plugin
    description: What your plugin does (one paragraph)
    version: "1.0.0"
    category: evaluation          # Must match a key in 'categories'
    scope: sdlc                   # generic | sdlc | team (default: sdlc) — see "Plugin scope"
    tags: [tag1, tag2]
    author:
      name: your-name
    license: Apache-2.0
    source:
      type: github
      repo: opendatahub-io/your-repo
      ref: main
    skills:
      - name: your-skill
        description: What this skill does
        user-invocable: true
    harnesses:
      claude-code:
        install: "/plugin install your-plugin@opendatahub-skills"
      generic:
        skill_format: markdown
        skill_dir: skills/
        entry_point: "skills/{skill_name}/SKILL.md"
    depends_on: []
```

For repos without `plugin.json`, add `strict: false` and `skills_dir`:
```yaml
    strict: false
    skills_dir: .claude/skills
```

The `user-invocable` field mirrors the [native Claude Code SKILL.md frontmatter field](https://code.claude.com/docs/en/skills#frontmatter-reference). Set it to `false` for internal skills that are called only by other skills/agents in the background — they will be hidden from the generated catalog. The registry value is catalog-only, so to actually hide the skill from the `/` menu in Claude Code you must also set `user-invocable: false` in the SKILL.md frontmatter in your source repo.

### Plugin scope

The optional `scope` field declares how reusable the plugin is. It is catalog-only metadata — it is **not** propagated to `marketplace.json` and does not affect installation (every plugin remains installable by anyone via `/plugin install`). It only controls how the plugin is labeled and organized in the catalog and docs site.

| Scope | Meaning | Example |
|-------|---------|---------|
| `generic` | Works anywhere, for any user or project | `agent-eval-harness` |
| `sdlc` (default) | RHOAI/ODH-wide, reusable across teams | `rfe-creator`, `assess-rfe` |
| `team` | Hardcoded to one team's setup (project keys, custom fields, labels) — not usable by others without modification | a team's JIRA-hygiene skill |

**Prefer making skills reusable.** If a skill only hardcodes team-specific values (project key, team ID, component, custom-field IDs) out of convenience, consider externalizing those into config or env vars so it can be `sdlc`-scoped and shared. Mark `scope: team` only when the skill genuinely serves a single team.

`generic` and `team` plugins are labeled on the site; `team` plugins are listed in a dedicated "Team-Specific" section rather than mixed into function categories. Always use a **function-based** `category` (what the skill does) regardless of scope — do not create team-named categories. Team identity belongs in `tags` and `scope`.

### 3. Regenerate Artifacts

After editing `registry.yaml`, validate and regenerate artifacts so CI stays in sync (same sequence as `CLAUDE.md`):

```bash
pip install pyyaml jsonschema  # once, if dependencies are missing
python3 scripts/validate_registry.py
python3 scripts/sync_marketplace.py
python3 scripts/generate_catalog.py
python3 scripts/generate_site.py
```

Commit generated updates under `.claude-plugin/marketplace.json`, `catalog.md`, and `site/` with your PR.

### Local Hooks

Install the same contract and `skill-linter` checks used in CI:

```bash
python3 -m pip install pre-commit
pre-commit install
```

The hooks validate staged `registry.yaml` changes and run pinned `skill-linter` checks against the referenced source skills. You also need Node.js 22 or newer available locally because `skill-linter` requires Node 22.

`config/skill-linter-registry.json` may downgrade an occasionally noisy rule to warning when permission-documentation text would otherwise false-positive, so you can still see warning-level linter output while the hook passes.

When you add a skill or change an existing skill's registry entry (compared against `HEAD` for pre-commit or the configured base ref in CI), include a canonical `contract` block on that skill plus accurate `contract.source_assertions` paths into the upstream repository; CI and hooks enforce this for touched skills.

### Choosing Canonical Contracts

Treat the `contract` block as a contributor-facing optimization spec, not a bag of tags. Keep it deliberate and minimal.

Use the generated canonical reference in [`catalog.md`](catalog.md#canonical-contract-system) for the full glossary of functions, metrics, and measures. In `CONTRIBUTING.md`, focus on these decision rules:

- Pick 1-2 `functions` that describe the published job-to-be-done, not an internal implementation step.
- Pick the smallest metric set that captures what a downstream optimizer should improve without changing the skill's purpose.
- Declare `measure` explicitly for every metric. Prefer `deterministic`, then `verifier_backed`, and use `judge` only when rubric-based evaluation is genuinely necessary.
- When `measure: judge`, include a stable `rubric_ref`. When `measure: verifier_backed`, include `verifier_ref`.
- Use `success_conditions`, `invariants`, and `source_assertions` to document what must remain fixed while the skill is optimized.
- Reserve `output_quality` for genuinely judge-only artifact quality; it always needs a rubric, and `calibration_ref`, `trials`, and `success_mode` become important once the metric is used for repeatable optimization rather than one-off review.

### 4. CI Validation

CI runs on pull requests and pushes to `main`. It automatically:
- Validates `registry.yaml` against the JSON Schema and touched-skill contract rules (diff-aware vs the PR base branch or prior push commit).
- Runs pinned `skill-linter` on skills you changed when they declare GitHub `source` and `contract.source_assertions`.
- Checks that referenced GitHub repos are reachable and that expected manifests or paths resolve as validated by `scripts/validate_registry.py`.

### 5. Review and Merge

Once CI passes and the PR is reviewed, it will be merged and the plugin will be available to all users who have added this marketplace.

## Updating a Plugin Version

Plugin versions are checked automatically every week. If you bump the `version` field in your repo's `plugin.json`, a PR will be auto-created to update `registry.yaml`.

You can also manually update the `version` field in `registry.yaml` and submit a PR.

## Adding a New Category

Add the category to the `categories` map in `registry.yaml`:

```yaml
categories:
  your-category:
    name: Your Category Name
    description: What plugins in this category do
```
