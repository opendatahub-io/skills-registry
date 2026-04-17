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

### 3. Regenerate Artifacts

After editing `registry.yaml`, regenerate the marketplace and catalog:

```bash
pip install pyyaml jsonschema
python3 scripts/sync_marketplace.py
python3 scripts/generate_catalog.py
```

Commit the updated `marketplace.json` and `catalog.md` with your PR.

### 4. CI Validation

The PR will automatically:
- Validate `registry.yaml` against the JSON Schema
- Check that your GitHub repo is accessible
- Clone your repo and verify `plugin.json` and `SKILL.md` files exist

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
