# Git Source Type Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Support non-GitHub source types in the registry by adding a `type: git` source with an explicit `url` field, while keeping `type: github` as ergonomic sugar.

**Architecture:** Add three helper functions to `registry_contracts.py` (`source_clone_url`, `source_display_name`, `source_browse_url`) that centralize URL derivation. Update the JSON Schema with conditional validation. Modify all scripts to use helpers instead of hardcoded GitHub URLs. TDD throughout.

**Tech Stack:** Python 3.12, JSON Schema (Draft 2020-12), PyYAML, jsonschema, unittest

---

### Task 1: Add helper functions to `registry_contracts.py`

**Files:**
- Modify: `scripts/registry_contracts.py` (add functions after line 68)
- Test: `tests/test_registry_contracts.py`

- [ ] **Step 1: Write failing tests for `source_clone_url`**

Add to `tests/test_registry_contracts.py`:

```python
from scripts.registry_contracts import (
    SkillKey,
    detect_touched_skills,
    load_registry_from_ref,
    load_staged_registry,
    source_browse_url,
    source_clone_url,
    source_display_name,
)


class SourceHelperTests(unittest.TestCase):
    def test_source_clone_url_github(self):
        source = {"type": "github", "repo": "opendatahub-io/rfe-creator"}
        self.assertEqual("https://github.com/opendatahub-io/rfe-creator.git", source_clone_url(source))

    def test_source_clone_url_git(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin.git"}
        self.assertEqual("https://gitlab.corp.example.com/team/my-plugin.git", source_clone_url(source))

    def test_source_clone_url_unsupported_type_raises(self):
        with self.assertRaises(ValueError):
            source_clone_url({"type": "npm", "repo": "foo"})

    def test_source_display_name_github(self):
        source = {"type": "github", "repo": "opendatahub-io/rfe-creator"}
        self.assertEqual("opendatahub-io/rfe-creator", source_display_name(source))

    def test_source_display_name_git_strips_scheme_and_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin.git"}
        self.assertEqual("gitlab.corp.example.com/team/my-plugin", source_display_name(source))

    def test_source_display_name_git_no_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin"}
        self.assertEqual("gitlab.corp.example.com/team/my-plugin", source_display_name(source))

    def test_source_browse_url_github(self):
        source = {"type": "github", "repo": "opendatahub-io/rfe-creator"}
        self.assertEqual("https://github.com/opendatahub-io/rfe-creator", source_browse_url(source))

    def test_source_browse_url_git_strips_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin.git"}
        self.assertEqual("https://gitlab.corp.example.com/team/my-plugin", source_browse_url(source))

    def test_source_browse_url_git_no_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin"}
        self.assertEqual("https://gitlab.corp.example.com/team/my-plugin", source_browse_url(source))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_registry_contracts.SourceHelperTests -v`
Expected: FAIL with ImportError (functions don't exist yet)

- [ ] **Step 3: Implement the three helper functions**

Add to `scripts/registry_contracts.py` after line 68 (after `PLUGIN_FIELDS_THAT_TOUCH_ALL_SKILLS`):

```python
import re as _re

_SCHEME_RE = _re.compile(r"^https?://")
GIT_CLONE_TYPES = frozenset({"github", "git"})


def source_clone_url(source: dict) -> str:
    """Return the git clone URL for a plugin source entry."""
    source_type = source.get("type")
    if source_type == "github":
        return f"https://github.com/{source['repo']}.git"
    if source_type == "git":
        return source["url"]
    raise ValueError(f"unsupported source type for cloning: {source_type!r}")


def source_display_name(source: dict) -> str:
    """Return a human-readable display name (scheme-stripped, no trailing .git)."""
    source_type = source.get("type")
    if source_type == "github":
        return source["repo"]
    if source_type == "git":
        url = source["url"]
        name = _SCHEME_RE.sub("", url)
        if name.endswith(".git"):
            name = name[:-4]
        return name
    return source.get("repo") or source.get("url") or "<unknown>"


def source_browse_url(source: dict) -> str:
    """Return a browsable URL for linking in markdown."""
    source_type = source.get("type")
    if source_type == "github":
        return f"https://github.com/{source['repo']}"
    if source_type == "git":
        url = source["url"]
        if url.endswith(".git"):
            return url[:-4]
        return url
    return source.get("url") or f"https://github.com/{source.get('repo', '')}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_registry_contracts.SourceHelperTests -v`
Expected: PASS (all 10 tests)

- [ ] **Step 5: Run full test suite to check for regressions**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: All existing tests still pass

- [ ] **Step 6: Commit**

```bash
git add scripts/registry_contracts.py tests/test_registry_contracts.py
git commit -S -s -m "feat: add source URL helper functions for git source type (#74)

Add source_clone_url, source_display_name, and source_browse_url to
registry_contracts.py. These centralize URL derivation for both
type: github (inferred from repo slug) and type: git (explicit url).

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: Update JSON Schema to support `type: git`

**Files:**
- Modify: `schema/registry.schema.json:390-418`
- Test: `tests/test_validate_registry.py`

- [ ] **Step 1: Write failing schema tests**

Add to `tests/test_validate_registry.py` in `SchemaTests`:

```python
    def test_schema_accepts_git_source_with_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.corp.example.com/team/my-plugin.git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_rejects_git_source_without_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("url" in error for error in errors), errors)

    def test_schema_rejects_github_source_without_repo(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "github",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("repo" in error for error in errors), errors)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_validate_registry.SchemaTests.test_schema_accepts_git_source_with_url tests.test_validate_registry.SchemaTests.test_schema_rejects_git_source_without_url tests.test_validate_registry.SchemaTests.test_schema_rejects_github_source_without_repo -v`
Expected: `test_schema_accepts_git_source_with_url` FAILs (git not in enum), the other two may pass or fail depending on current required fields

- [ ] **Step 3: Update the schema**

Modify `schema/registry.schema.json` lines 390-418. Replace the `source` definition:

```json
"source": {
  "type": "object",
  "required": ["type"],
  "additionalProperties": false,
  "properties": {
    "type": {
      "type": "string",
      "enum": ["github", "git", "git-subdir", "npm", "local"],
      "description": "Source type"
    },
    "repo": {
      "type": "string",
      "description": "Repository identifier (e.g., owner/repo) — required for github type"
    },
    "url": {
      "type": "string",
      "format": "uri",
      "description": "Clone URL — required for git type"
    },
    "ref": {
      "type": "string",
      "description": "Git branch, tag, or ref"
    },
    "sha": {
      "type": "string",
      "pattern": "^[0-9a-f]{40}$",
      "description": "Exact commit SHA"
    },
    "path": {
      "type": "string",
      "description": "Subdirectory path (for git-subdir type)"
    }
  },
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
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_validate_registry.SchemaTests -v`
Expected: All schema tests pass including the three new ones

- [ ] **Step 5: Run full test suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add schema/registry.schema.json tests/test_validate_registry.py
git commit -S -s -m "feat: add git source type to registry schema (#74)

Add 'git' to source type enum and 'url' property. Use conditional
validation (if/then) to require 'repo' for github and 'url' for git.
Change source required from ['type', 'repo'] to ['type'].

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: Update `validate_registry.py` to support git sources

**Files:**
- Modify: `scripts/validate_registry.py:253-348`
- Test: `tests/test_validate_registry.py`

- [ ] **Step 1: Write failing tests**

Add to `tests/test_validate_registry.py` in `RemotePluginValidationTests`:

```python
    @mock.patch("subprocess.run")
    def test_check_sources_uses_ls_remote_for_git_type(self, run_mock):
        run_mock.return_value = subprocess.CompletedProcess(
            ["git", "ls-remote"], 0, stdout="", stderr=""
        )
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
        }

        errors = self.validate_registry.check_sources(registry)

        self.assertEqual([], errors)
        run_mock.assert_called_once()
        cmd = run_mock.call_args[0][0]
        self.assertEqual(cmd[0], "git")
        self.assertIn("ls-remote", cmd)

    @mock.patch("subprocess.run")
    def test_validate_remote_plugin_accepts_git_type(self, run_mock):
        run_mock.return_value = subprocess.CompletedProcess(
            ["git", "clone"], 0, stdout="", stderr=""
        )
        plugin = {
            "name": "git-plugin",
            "source": {
                "type": "git",
                "url": "https://gitlab.example.com/team/plugin.git",
                "ref": "main",
            },
        }

        # Will fail on clone (mock returns empty dir) but should not
        # skip due to source type
        errors = self.validate_registry.validate_remote_plugin(plugin)

        self.assertTrue(run_mock.called)
        cmd = run_mock.call_args[0][0]
        self.assertIn("https://gitlab.example.com/team/plugin.git", cmd)
```

Add `import subprocess` to the imports at top of `tests/test_validate_registry.py` if not already present.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_validate_registry.RemotePluginValidationTests -v`
Expected: FAIL — `check_sources` skips non-github, `validate_remote_plugin` skips non-github

- [ ] **Step 3: Update `check_sources` in `validate_registry.py`**

Replace lines 253-271:

```python
def check_sources(registry: dict) -> list[str]:
    """Check that source repos are accessible."""
    from scripts.registry_contracts import GIT_CLONE_TYPES, source_clone_url

    errors = []
    for plugin in registry.get("plugins", []):
        source = plugin.get("source")
        if not source:
            continue
        source_type = source.get("type")
        if source_type not in GIT_CLONE_TYPES:
            continue
        name = plugin.get("name", "<unknown>")
        if source_type == "github":
            repo = source.get("repo")
            if not repo:
                continue
            result = subprocess.run(
                ["gh", "api", f"repos/{repo}", "--silent"],
                capture_output=True, text=True,
            )
        else:
            try:
                clone_url = source_clone_url(source)
            except (ValueError, KeyError):
                errors.append(f"  Plugin '{name}': invalid source configuration")
                continue
            result = subprocess.run(
                ["git", "ls-remote", "--exit-code", "--quiet", clone_url],
                capture_output=True, text=True,
            )
        if result.returncode != 0:
            errors.append(f"  Plugin '{name}': source not accessible")
        else:
            print(f"  OK: {name}")
    return errors
```

- [ ] **Step 4: Update `validate_remote_plugin` in `validate_registry.py`**

Replace the source type check and clone URL construction (around lines 288-308). Change:

```python
    source = plugin.get("source")
    if not source or source.get("type") != "github":
        return errors
```

to:

```python
    from scripts.registry_contracts import GIT_CLONE_TYPES, source_clone_url

    source = plugin.get("source")
    if not source or source.get("type") not in GIT_CLONE_TYPES:
        return errors
```

And replace the hardcoded clone URL:

```python
    clone_url = f"https://github.com/{repo}.git"
```

with:

```python
    try:
        clone_url = source_clone_url(source)
    except (ValueError, KeyError):
        errors.append(f"  Plugin '{plugin['name']}': invalid source configuration")
        return errors
```

Remove the `repo = source["repo"]` line that preceded the old clone_url construction (the `repo` variable is no longer needed for the URL).

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_validate_registry.RemotePluginValidationTests -v`
Expected: All pass

- [ ] **Step 6: Run full test suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: All pass

- [ ] **Step 7: Commit**

```bash
git add scripts/validate_registry.py tests/test_validate_registry.py
git commit -S -s -m "feat: validate_registry supports git source type (#74)

check_sources uses git ls-remote for type: git, keeps gh api for
type: github. validate_remote_plugin uses source_clone_url helper
for both types.

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 4: Update `run_skill_linter.py` to support git sources

**Files:**
- Modify: `scripts/run_skill_linter.py:180-267`
- Test: `tests/test_run_skill_linter.py`

- [ ] **Step 1: Write failing tests**

Add to `tests/test_run_skill_linter.py` in `SkillLinterWrapperTests`:

```python
    def test_skill_is_skill_linter_candidate_accepts_git_type(self):
        plugin_git = {
            "name": "p",
            "source": {"type": "git", "url": "https://gitlab.example.com/t/p.git"},
        }
        skill_ok = {
            "name": "t",
            "contract": {"source_assertions": {"skill_path": ".claude/skills/t/SKILL.md"}},
        }
        self.assertTrue(skill_is_skill_linter_candidate(plugin_git, skill_ok))

    def test_skill_is_skill_linter_candidate_rejects_git_without_url(self):
        plugin_git = {"name": "p", "source": {"type": "git"}}
        skill_ok = {
            "name": "t",
            "contract": {"source_assertions": {"skill_path": ".claude/skills/t/SKILL.md"}},
        }
        self.assertFalse(skill_is_skill_linter_candidate(plugin_git, skill_ok))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_run_skill_linter.SkillLinterWrapperTests.test_skill_is_skill_linter_candidate_accepts_git_type tests.test_run_skill_linter.SkillLinterWrapperTests.test_skill_is_skill_linter_candidate_rejects_git_without_url -v`
Expected: `test_skill_is_skill_linter_candidate_accepts_git_type` FAILs (git type not accepted)

- [ ] **Step 3: Update `skill_is_skill_linter_candidate`**

In `scripts/run_skill_linter.py`, replace lines 193-199:

```python
    source = plugin.get("source") or {}
    if not isinstance(source, dict) or source.get("type") != "github":
        return False
    repo = source.get("repo")
    if not isinstance(repo, str) or not repo.strip():
        return False
```

with:

```python
    source = plugin.get("source") or {}
    if not isinstance(source, dict):
        return False
    source_type = source.get("type")
    if source_type not in GIT_CLONE_TYPES:
        return False
    if source_type == "github":
        repo = source.get("repo")
        if not isinstance(repo, str) or not repo.strip():
            return False
    elif source_type == "git":
        url = source.get("url")
        if not isinstance(url, str) or not url.strip():
            return False
```

Add `GIT_CLONE_TYPES` to the imports from `scripts.registry_contracts` at the top of the file (line 22-32):

```python
from scripts.registry_contracts import (  # noqa: E402
    GIT_CLONE_TYPES,
    SKILL_LINTER_VERSION,
    SkillKey,
    ...
)
```

- [ ] **Step 4: Update `_ensure_github_repo` -> `_ensure_repo`**

Rename the function (line 214) and replace the clone URL construction (line 217):

```python
def _ensure_repo(source: dict) -> Path:
    clone_url = source_clone_url(source)
    source_type = source.get("type")
    if source_type == "github":
        repo = source["repo"]
        ref = normalize_git_ref(source.get("ref", "main"))
    else:
        repo = source_display_name(source)
        ref = normalize_git_ref(source.get("ref", "main"))
```

Add `source_clone_url` and `source_display_name` to the imports from `scripts.registry_contracts`.

Update the `_cache_destination` call to use `source_display_name(source)` instead of `repo`:

```python
    destination = _cache_destination(source_display_name(source), ref)
```

Replace `clone_url = f"https://github.com/{repo}.git"` with just using the `clone_url` from above.

- [ ] **Step 5: Update `_run_one_skill` to use `_ensure_repo`**

Replace the github-only gate (lines 295-319) in `_run_one_skill`. Change:

```python
    source = plugin.get("source") or {}
    if not isinstance(source, dict) or source.get("type") != "github":
        print(
            f"ERROR: Plugin '{plug_name}' skill '{ski_name}' "
            "has contract source_assertions but source is not type 'github'",
            file=sys.stderr,
        )
        return 1
```

to:

```python
    source = plugin.get("source") or {}
    if not isinstance(source, dict) or source.get("type") not in GIT_CLONE_TYPES:
        print(
            f"ERROR: Plugin '{plug_name}' skill '{ski_name}' "
            "has contract source_assertions but source type is not cloneable",
            file=sys.stderr,
        )
        return 1
```

Replace:

```python
    repo = source.get("repo")
    if not isinstance(repo, str) or not repo.strip():
        print(
            f"ERROR: Plugin '{plug_name}' is missing source.repo.",
            file=sys.stderr,
        )
        return 1
```

with:

```python
    try:
        _ = source_clone_url(source)
    except (ValueError, KeyError):
        print(
            f"ERROR: Plugin '{plug_name}' has invalid source configuration.",
            file=sys.stderr,
        )
        return 1
```

Change `repo_root = _ensure_github_repo(repo, plugin_ref)` to `repo_root = _ensure_repo(source)`.

Update the print line: replace `repo={repo} ref={plugin_ref}` with `source={source_display_name(source)}`:

```python
    print(f"Running skill-linter for {plug_name}/{ski_name} (source={source_display_name(source)})...")
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_run_skill_linter -v`
Expected: All pass

- [ ] **Step 7: Run full test suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: All pass

- [ ] **Step 8: Commit**

```bash
git add scripts/run_skill_linter.py tests/test_run_skill_linter.py
git commit -S -s -m "feat: skill linter supports git source type (#74)

Rename _ensure_github_repo to _ensure_repo. Use source_clone_url and
source_display_name helpers. Accept type: git alongside type: github
for linter candidacy.

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5: Update `check_versions.py` to support git sources

**Files:**
- Modify: `scripts/check_versions.py:42-63,76-79`

- [ ] **Step 1: Add `fetch_remote_version_via_clone` function**

Add after `fetch_remote_version` (line 63):

```python
def fetch_remote_version_via_clone(clone_url: str, ref: str = "main") -> str | None:
    """Fetch version from remote plugin.json via shallow clone."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", ref, "--", clone_url, tmpdir],
            capture_output=True, text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return None
        plugin_json = Path(tmpdir) / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            return None
        try:
            data = json.loads(plugin_json.read_text())
            return data.get("version")
        except (json.JSONDecodeError, OSError):
            return None
```

Add `import tempfile` and `from pathlib import Path` to the imports at the top (line 1-6). Also add:

```python
from scripts.registry_contracts import GIT_CLONE_TYPES, source_clone_url, normalize_git_ref
```

- [ ] **Step 2: Update the main loop to handle git sources**

Replace the source type check (lines 76-79):

```python
        if source.get("type") != "github":
            continue
```

with:

```python
        source_type = source.get("type")
        if source_type not in GIT_CLONE_TYPES:
            continue
```

Replace the remote version fetch call (line 90):

```python
        remote = fetch_remote_version(repo, source.get("ref", "main"))
```

with:

```python
        if source_type == "github":
            remote = fetch_remote_version(repo, source.get("ref", "main"))
        else:
            try:
                clone_url = source_clone_url(source)
                ref = normalize_git_ref(source.get("ref", "main"))
            except (ValueError, KeyError):
                print(f"  SKIP: {name} (invalid source configuration)")
                continue
            remote = fetch_remote_version_via_clone(clone_url, ref)
```

Note: the `repo` variable used for `fetch_remote_version` is still read from `source.get("repo")` on line 85. For git type, `repo` will be `None`, which is fine because that branch uses `source_clone_url` instead.

- [ ] **Step 3: Run validation to check nothing broke**

Run: `python3 scripts/check_versions.py --dry-run`
Expected: Runs and shows current plugin versions (all github, so existing path)

- [ ] **Step 4: Commit**

```bash
git add scripts/check_versions.py
git commit -S -s -m "feat: check_versions supports git source type (#74)

For type: git, shallow clone to a temp directory to read plugin.json
instead of using the GitHub API. Weekly job, performance not critical.

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: Update `generate_catalog.py` to use source helpers

**Files:**
- Modify: `scripts/generate_catalog.py:216`
- Test: `tests/test_generate_catalog.py`

- [ ] **Step 1: Write failing test**

Add to `tests/test_generate_catalog.py`:

```python
class CatalogGitSourceTests(unittest.TestCase):
    def test_catalog_renders_git_source_browse_link(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
        }

        content = generate_catalog.generate_catalog(registry)

        self.assertIn("[gitlab.example.com/team/plugin](https://gitlab.example.com/team/plugin)", content)
        self.assertNotIn("github.com", content.split("Quick Start")[1])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_generate_catalog.CatalogGitSourceTests -v`
Expected: FAIL — current code builds `https://github.com/{repo}` which will fail on missing repo key or produce wrong URL

- [ ] **Step 3: Update `render_plugin` in `generate_catalog.py`**

Add import at top of file (after line 23):

```python
from scripts.registry_contracts import source_browse_url, source_display_name
```

Replace line 216:

```python
        meta_parts.append(f"[{repo}](https://github.com/{repo})")
```

with:

```python
        display = source_display_name(plugin["source"])
        browse = source_browse_url(plugin["source"])
        meta_parts.append(f"[{display}]({browse})")
```

Remove the `repo = plugin["source"].get("repo", "")` line (around line 189) and the `if repo:` guard (around line 215-216). Replace them with:

```python
    source = plugin["source"]
    source_type = source.get("type", "")
```

And change the guard to:

```python
    if source_type in ("github", "git"):
        display = source_display_name(source)
        browse = source_browse_url(source)
        meta_parts.append(f"[{display}]({browse})")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_generate_catalog -v`
Expected: All pass

- [ ] **Step 5: Regenerate catalog.md and verify**

Run: `python3 scripts/generate_catalog.py`
Expected: Generates successfully. Existing github links unchanged (since all current plugins are github).

- [ ] **Step 6: Commit**

```bash
git add scripts/generate_catalog.py tests/test_generate_catalog.py
git commit -S -s -m "feat: catalog generator supports git source type (#74)

Use source_browse_url and source_display_name helpers instead of
hardcoded GitHub URL construction.

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7: Update `generate_site.py` to use source helpers

**Files:**
- Modify: `scripts/generate_site.py:398,869`
- Test: `tests/test_generate_site.py`

- [ ] **Step 1: Write failing test**

Add to `tests/test_generate_site.py`:

```python
class SiteGitSourceTests(unittest.TestCase):
    def test_plugin_page_renders_git_source_link(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
        }

        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)

        self.assertIn("gitlab.example.com/team/plugin", page)
        self.assertIn("https://gitlab.example.com/team/plugin", page)
        self.assertNotIn("https://github.com/", page)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_generate_site.SiteGitSourceTests -v`
Expected: FAIL — current code builds `https://github.com/{repo}`

- [ ] **Step 3: Update `generate_plugin_page`**

Add imports at top (after line 27):

```python
from scripts.registry_contracts import (
    ...
    source_browse_url,
    source_display_name,
)
```

Replace line 398:

```python
    if repo:
        meta.append(f"    - **Repository**: [{repo}](https://github.com/{repo})")
```

with:

```python
    source = plugin.get("source", {})
    source_type = source.get("type", "")
    if source_type in ("github", "git"):
        display = source_display_name(source)
        browse = source_browse_url(source)
        meta.append(f"    - **Repository**: [{display}]({browse})")
```

Remove the `repo = plugin.get("source", {}).get("repo", "")` line earlier in the function (around line 364) since we now use `source` directly. Keep other uses of `repo` variable if they exist in the function — check and replace each.

- [ ] **Step 4: Update `generate_llms_full_txt`**

Replace line 869:

```python
        if repo:
            lines.append(f"**Repository**: https://github.com/{repo}")
```

with:

```python
        source = p.get("source", {})
        source_type = source.get("type", "")
        if source_type in ("github", "git"):
            lines.append(f"**Repository**: {source_browse_url(source)}")
```

Remove the `repo = p.get("source", {}).get("repo", "")` line (around line 859).

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_generate_site -v`
Expected: All pass

- [ ] **Step 6: Regenerate site and verify**

Run: `python3 scripts/generate_site.py`
Expected: Generates successfully, existing github links unchanged.

- [ ] **Step 7: Commit**

```bash
git add scripts/generate_site.py tests/test_generate_site.py
git commit -S -s -m "feat: site generator supports git source type (#74)

Use source_browse_url and source_display_name helpers in plugin pages
and llms-full.txt instead of hardcoded GitHub URL construction.

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 8: Update `sync_marketplace.py` to emit `url` for git sources

**Files:**
- Modify: `scripts/sync_marketplace.py:44-55`

- [ ] **Step 1: Update `plugin_to_marketplace_entry`**

Replace lines 46-55 (the source mapping block):

```python
    # Map source
    source = plugin["source"]
    entry["source"] = {
        "source": source["type"],
        "repo": source["repo"],
    }
    if "ref" in source:
        entry["source"]["ref"] = source["ref"]
    if "sha" in source:
        entry["source"]["sha"] = source["sha"]
    if "path" in source:
        entry["source"]["path"] = source["path"]
```

with:

```python
    # Map source
    source = plugin["source"]
    mapped = {"source": source["type"]}
    if "repo" in source:
        mapped["repo"] = source["repo"]
    if "url" in source:
        mapped["url"] = source["url"]
    if "ref" in source:
        mapped["ref"] = source["ref"]
    if "sha" in source:
        mapped["sha"] = source["sha"]
    if "path" in source:
        mapped["path"] = source["path"]
    entry["source"] = mapped
```

- [ ] **Step 2: Regenerate marketplace.json and verify no diff**

Run: `python3 scripts/sync_marketplace.py`
Expected: No changes to marketplace.json (all current plugins are github, so `repo` is still emitted).

- [ ] **Step 3: Run full test suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: All pass

- [ ] **Step 4: Commit**

```bash
git add scripts/sync_marketplace.py
git commit -S -s -m "feat: marketplace sync emits url for git source type (#74)

Pass through url field for type: git sources alongside the existing
repo field for type: github sources.

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 9: Regenerate all artifacts and run CI checks

**Files:**
- Regenerate: `.claude-plugin/marketplace.json`, `catalog.md`, `site/`

- [ ] **Step 1: Run validation**

Run: `python3 scripts/validate_registry.py`
Expected: PASSED

- [ ] **Step 2: Regenerate all artifacts**

Run: `python3 scripts/sync_marketplace.py && python3 scripts/generate_catalog.py && python3 scripts/generate_site.py`
Expected: All generate successfully

- [ ] **Step 3: Run full test suite**

Run: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
Expected: All pass

- [ ] **Step 4: Verify no unexpected diffs in generated files**

Run: `git diff --stat`
Expected: No changes (all current plugins are github, so generated files should be identical)

- [ ] **Step 5: Run linter**

Run: `python3 -m py_compile scripts/registry_contracts.py && python3 -m py_compile scripts/validate_registry.py && python3 -m py_compile scripts/run_skill_linter.py && python3 -m py_compile scripts/check_versions.py && python3 -m py_compile scripts/generate_catalog.py && python3 -m py_compile scripts/generate_site.py && python3 -m py_compile scripts/sync_marketplace.py`
Expected: All compile cleanly

---

### Task 10: Update documentation

**Files:**
- Modify: `CONTRIBUTING.md`
- Modify: `ARCHITECTURE.md`

- [ ] **Step 1: Update CONTRIBUTING.md**

In the "Add Your Entry to registry.yaml" section, after the existing `source:` example block, add a new subsection:

```markdown
For plugins hosted on non-GitHub forges (GitLab, Gitea, etc.), use `type: git` with an explicit `url`:
```yaml
    source:
      type: git
      url: https://gitlab.corp.example.com/team/your-repo.git
      ref: main
```
```

- [ ] **Step 2: Update ARCHITECTURE.md**

In the "Plugin Model" section, after the existing diagram showing `github` sources, add a paragraph:

```markdown
### Source Types

- **`type: github`** — shorthand for GitHub repos. Only requires `repo: owner/name`;
  clone and browse URLs are derived automatically.
- **`type: git`** — explicit clone URL for any git forge (GitLab, Gitea, Bitbucket, etc.).
  Requires `url` (the clone URL). Browse links strip the trailing `.git` suffix.
- **`type: git-subdir`** — subdirectory within a git repo (uses `path`).
- **`type: npm`** / **`type: local`** — non-git source types.
```

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md ARCHITECTURE.md
git commit -S -s -m "docs: document git source type in CONTRIBUTING and ARCHITECTURE (#74)

Add type: git example to CONTRIBUTING.md and a Source Types reference
section to ARCHITECTURE.md.

Assisted-by: Claude Opus 4.6 <noreply@anthropic.com>"
```
