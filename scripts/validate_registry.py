#!/usr/bin/env python3
"""Validate registry.yaml against the JSON Schema and check plugin sources.

Usage:
    python3 scripts/validate_registry.py                        # Schema validation only
    python3 scripts/validate_registry.py --check-sources        # Also check GitHub repos exist
    python3 scripts/validate_registry.py --diff origin/main     # Detect newly added plugins
    python3 scripts/validate_registry.py --validate-remote-plugins  # Clone and validate new plugins
    python3 scripts/validate_registry.py --staged               # Require contracts for skills changed vs HEAD (staged registry)
    python3 scripts/validate_registry.py --diff-base REF        # Require contracts for skills changed since REF
    python3 scripts/validate_registry.py --check-skill-names    # Check skill names against upstream SKILL.md
    python3 scripts/validate_registry.py --check-codex-manifests  # Warn on plugins missing .codex-plugin/plugin.json
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# Repo root must be on sys.path when this file is run as scripts/validate_registry.py
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent
_REPO_ROOT_STR = str(_REPO_ROOT)
sys.path[:] = [entry for entry in sys.path if entry != _REPO_ROOT_STR]
sys.path.insert(0, _REPO_ROOT_STR)

from scripts.registry_contracts import (  # noqa: E402
    CANONICAL_FUNCTIONS,
    CANONICAL_METRICS,
    GIT_CLONE_TYPES,
    GIT_CLONEABLE_TYPES,
    SkillKey,
    detect_touched_skills,
    iter_plugins,
    iter_skills,
    load_registry_from_ref,
    load_staged_registry,
    normalize_git_ref,
    redact_url,
    shallow_clone,
    source_clone_url,
    source_subdir,
)

try:
    import jsonschema
except ImportError:
    jsonschema = None


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_schema(path: str = "schema/registry.schema.json") -> dict:
    with open(path) as f:
        return json.load(f)


def validate_schema(registry: dict, schema: dict) -> list[str]:
    """Validate registry against JSON Schema. Returns list of errors."""
    if jsonschema is None:
        print("ERROR: jsonschema not installed, cannot validate schema", file=sys.stderr)
        sys.exit(1)

    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(registry), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"  {path}: {error.message}")
    return errors


def check_duplicates(registry: dict) -> list[str]:
    """Check for duplicate plugin names."""
    names = [p["name"] for p in registry.get("plugins", [])]
    seen = set()
    dupes = []
    for name in names:
        if name in seen:
            dupes.append(f"  Duplicate plugin name: {name}")
        seen.add(name)
    return dupes


def check_categories(registry: dict) -> list[str]:
    """Check that all plugin categories reference defined categories."""
    defined = set(registry.get("categories", {}).keys())
    errors = []
    for plugin in registry.get("plugins", []):
        cat = plugin.get("category")
        if cat and cat not in defined:
            errors.append(f"  Plugin '{plugin['name']}' references undefined category '{cat}'")
    return errors


def _detect_bundle_cycles(by_name: dict) -> list[str]:
    """Report cycles in the includes graph (each cycle once)."""
    errors: list[str] = []
    reported: set[frozenset] = set()

    def dfs(name: str, path: list[str]) -> None:
        if name in path:
            cycle = path[path.index(name):]
            if len(cycle) >= 2:  # self-reference is reported by the caller
                key = frozenset(cycle)
                if key not in reported:
                    reported.add(key)
                    errors.append(
                        "  includes cycle detected: "
                        + " -> ".join(cycle + [name]))
            return
        members = (by_name.get(name) or {}).get("includes") or []
        for member in members:
            if member in by_name:
                dfs(member, path + [name])

    for name, plugin in by_name.items():
        if plugin.get("includes"):
            dfs(name, [])
    return errors


def check_bundles(registry: dict) -> list[str]:
    """Validate bundle (meta-plugin) entries.

    A bundle declares ``includes`` naming other registry plugins. Because
    a bundle's displayed skill count is derived from its members (and it is
    excluded from registry-wide totals), it must not also carry its own count:
    no ``skills`` array and no ``skill_count``. Members must resolve to defined
    plugins, a bundle may not list itself, a member may not itself be a bundle
    (nesting is not supported), and the graph must be acyclic. For a leaf
    plugin, ``skill_count`` is a substitute for a ``skills`` array, so the two
    are mutually exclusive there as well.
    """
    plugins = registry.get("plugins", [])
    names = {p.get("name") for p in plugins}
    by_name = {p.get("name"): p for p in plugins}
    errors = []
    for plugin in plugins:
        name = plugin.get("name")
        # Presence-based, not truthiness-based: an explicit empty includes
        # or an empty skills array is still a contract violation.
        has_includes = "includes" in plugin
        members = plugin.get("includes") or []
        if has_includes and not members:
            errors.append(
                f"  Plugin '{name}' declares an empty includes list; "
                "omit the field or list at least one member")
        if not members:
            if "skill_count" in plugin and "skills" in plugin:
                errors.append(
                    f"  Plugin '{name}' declares both skill_count and a skills "
                    "array; use one (skill_count is for plugins that carry no "
                    "skills array)")
            continue
        if "skills" in plugin:
            errors.append(
                f"  Plugin '{name}' declares includes and a skills array; "
                "a bundle must not carry its own skills")
        if "skill_count" in plugin:
            errors.append(
                f"  Plugin '{name}' declares includes and skill_count; a "
                "bundle's count is derived from its members, remove skill_count")
        for member in members:
            if member == name:
                errors.append(f"  Plugin '{name}' lists itself in includes")
            elif member not in names:
                errors.append(
                    f"  Plugin '{name}' includes references undefined "
                    f"plugin '{member}'")
            elif by_name.get(member, {}).get("includes"):
                errors.append(
                    f"  Plugin '{name}' includes '{member}', which is itself a "
                    "bundle; nested bundles are not supported")
    errors.extend(_detect_bundle_cycles(by_name))
    return errors


def check_strict_consistency(registry: dict) -> list[str]:
    """Check that skills_dir is only used with strict: false."""
    errors = []
    for plugin in registry.get("plugins", []):
        name = plugin.get("name", "<unknown>")
        has_skills_dir = "skills_dir" in plugin
        strict = plugin.get("strict", True)

        if has_skills_dir and strict is not False:
            errors.append(
                f"  Plugin '{name}': skills_dir requires strict: false. "
                "Remove skills_dir or set strict: false"
            )
    return errors


_PLACEHOLDER_RE = re.compile(
    r"\b(TODO|TBD|FIXME|PLACEHOLDER|XXX)\b|\{\{[\s\S]*?\}\}|\[insert\b",
    re.IGNORECASE,
)


def _mapping(value) -> dict:
    if isinstance(value, dict):
        return value
    return {}


def has_placeholder_text(text: str) -> bool:
    """True if problem_statement is empty/whitespace or contains common placeholder markers."""
    if not isinstance(text, str):
        return True
    stripped = text.strip()
    if not stripped:
        return True
    return _PLACEHOLDER_RE.search(stripped) is not None


def get_plugin_label(plugin: dict) -> str:
    return plugin.get("name", "<unknown>")


def select_required_skills(args, current_registry: dict) -> tuple[set[SkillKey], list[str]]:
    """Return skills that require semantic contract validation, plus fatal selection errors."""

    registry_path = getattr(args, "registry", "registry.yaml")
    if getattr(args, "staged", False):
        try:
            before = load_registry_from_ref("HEAD", path=registry_path)
            after = load_staged_registry(path=registry_path)
        except (subprocess.CalledProcessError, RuntimeError, ValueError):
            return set(), [
                "  Could not read registry.yaml from git (HEAD or staged copy). "
                "Use --staged from a git repository with the registry file staged."
            ]
        return set(detect_touched_skills(before, after)), []
    if getattr(args, "diff_base", None):
        ref = args.diff_base
        try:
            before = load_registry_from_ref(ref, path=registry_path)
        except (subprocess.CalledProcessError, RuntimeError, ValueError):
            return set(), [
                f"  Could not load {registry_path} from git ref {ref!r} "
                "(missing ref or path not present at that revision)."
            ]
        return set(detect_touched_skills(before, current_registry)), []
    return set(), []


def check_skill_contracts(registry: dict, required_skills: set[SkillKey]) -> list[str]:
    errors: list[str] = []
    for plugin in iter_plugins(registry):
        plugin_name = get_plugin_label(plugin)
        # Contracts are required only for cloneable/verifiable sources
        # (github/git) -- the same boundary skill-linter and skill-name-drift
        # use. git-subdir/npm/local skills are delegated: their source cannot be
        # cloned and their source_assertions cannot be resolved, so a contract
        # on them would be unverifiable metadata. Such plugins may list skills
        # (name + description) for display without a contract block.
        source = plugin.get("source") or {}
        if source.get("type") not in GIT_CLONE_TYPES:
            continue
        for skill in iter_skills(plugin):
            skill_name = skill.get("name", "<unknown>")
            key = SkillKey(plugin_name, skill_name)

            if key not in required_skills:
                continue

            contract = skill.get("contract")

            if not isinstance(contract, dict):
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}' requires contract metadata"
                )
                continue

            functions = contract.get("functions", [])
            metrics = contract.get("metrics", [])
            source_assertions = _mapping(contract.get("source_assertions"))

            if len(functions) != len(set(functions)):
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}': duplicate function assignment"
                )
            if any(function_name not in CANONICAL_FUNCTIONS for function_name in functions):
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}': unknown function value"
                )

            metric_ids = [metric.get("id") for metric in metrics if isinstance(metric, dict)]
            if len(metric_ids) != len(set(metric_ids)):
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}': duplicate metric assignment"
                )
            if any(metric_id not in CANONICAL_METRICS for metric_id in metric_ids):
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}': unknown metric value"
                )

            if has_placeholder_text(contract.get("problem_statement", "")):
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}': "
                    "problem_statement contains placeholder content"
                )

            for metric in metrics:
                if not isinstance(metric, dict):
                    continue
                rubric_ref_val = metric.get("rubric_ref")
                has_rubric_ref = isinstance(rubric_ref_val, str) and bool(rubric_ref_val.strip())
                metric_id = metric.get("id")
                if metric_id == "output_quality":
                    if not has_rubric_ref:
                        errors.append(
                            f"  Plugin '{plugin_name}' skill '{skill_name}': "
                            "output_quality metric requires a non-empty rubric_ref"
                        )
                elif metric.get("measure") == "judge" and not has_rubric_ref:
                    errors.append(
                        f"  Plugin '{plugin_name}' skill '{skill_name}': "
                        "judge metrics require rubric_ref"
                    )
                if metric.get("measure") == "verifier_backed" and not metric.get(
                    "verifier_ref"
                ):
                    errors.append(
                        f"  Plugin '{plugin_name}' skill '{skill_name}': "
                        "verifier-backed metrics require verifier_ref"
                    )

            skill_path_val = source_assertions.get("skill_path")
            if not isinstance(skill_path_val, str) or not skill_path_val.strip():
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}': "
                    "source_assertions.skill_path is required"
                )
            elif Path(skill_path_val.strip()).name != "SKILL.md":
                errors.append(
                    f"  Plugin '{plugin_name}' skill '{skill_name}': "
                    "source_assertions.skill_path must name a SKILL.md file "
                    f"(got basename {Path(skill_path_val.strip()).name!r})"
                )

    return errors


def check_sources(registry: dict) -> list[str]:
    """Check that source repos are accessible.

    Covers every cloneable source, including git-subdir: the whole repo is what
    must be reachable, so `git ls-remote` runs against the repo clone URL (the
    subdirectory itself is verified by the clone-based checks).
    """
    errors = []
    for plugin in registry.get("plugins", []):
        source = plugin.get("source")
        if not source:
            continue
        source_type = source.get("type")
        if source_type not in GIT_CLONEABLE_TYPES:
            continue
        name = plugin.get("name", "<unknown>")
        if source_type == "github":
            repo = source.get("repo")
            if not repo:
                continue
            result = subprocess.run(
                ["gh", "api", f"repos/{repo}", "--silent"],
                capture_output=True, text=True,
                timeout=30,
            )
        else:
            try:
                clone_url = source_clone_url(source)
            except (ValueError, KeyError):
                errors.append(f"  Plugin '{name}': invalid source configuration")
                continue
            result = subprocess.run(
                ["git", "ls-remote", "--exit-code", "--quiet", "--", clone_url],
                capture_output=True, text=True,
                timeout=30,
            )
        if result.returncode != 0:
            errors.append(f"  Plugin '{name}': source not accessible")
        else:
            print(f"  OK: {name}")
    return errors


def diff_plugins(registry: dict, base_ref: str) -> list[str]:
    """Find plugin names added since base_ref."""
    try:
        base_registry = load_registry_from_ref(base_ref)
    except (subprocess.CalledProcessError, RuntimeError, ValueError):
        print(f"WARNING: could not read registry.yaml from {base_ref}, treating all as new",
              file=sys.stderr)
        return [p["name"] for p in registry.get("plugins", [])]
    base_names = {p["name"] for p in base_registry.get("plugins", [])}
    current_names = {p["name"] for p in registry.get("plugins", [])}
    new_names = sorted(current_names - base_names)
    return new_names


def _plugin_root_in_clone(repo_path: Path, source: dict) -> Path | None:
    """Root of the plugin inside a cloned repo.

    For git-subdir this is ``repo_path/<path>``; for whole-repo sources it is
    ``repo_path`` itself. Returns ``None`` if the subdirectory would escape the
    clone root — the schema does not constrain ``source.path``, so a ``..``
    component is rejected here (CWE-22).
    """
    subdir = source_subdir(source)
    if not subdir:
        return repo_path
    root = repo_path.resolve()
    try:
        candidate = (repo_path / subdir).resolve()
    except OSError:
        return None
    if candidate != root and not candidate.is_relative_to(root):
        return None
    return candidate


def validate_remote_plugin(plugin: dict) -> list[str]:
    """Clone a plugin repo and validate its structure.

    For git-subdir sources the plugin lives in a subdirectory of the clone; all
    structure checks are rooted there rather than at the repository root.
    """
    errors = []
    source = plugin.get("source")
    if not source or source.get("type") not in GIT_CLONEABLE_TYPES:
        return errors

    try:
        ref = normalize_git_ref(source.get("ref", "main"))
    except ValueError:
        errors.append(f"  Plugin '{plugin['name']}': invalid source.ref")
        return errors
    strict = plugin.get("strict", True)

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            clone_url = source_clone_url(source)
        except (ValueError, KeyError):
            errors.append(f"  Plugin '{plugin['name']}': invalid source configuration")
            return errors
        try:
            result = shallow_clone(clone_url, ref, tmpdir)
        except RuntimeError as exc:
            errors.append(f"  Plugin '{plugin['name']}': {redact_url(str(exc))}")
            return errors
        if result.returncode != 0:
            errors.append(
                f"  Plugin '{plugin['name']}': failed to clone {redact_url(clone_url)} (ref={ref})"
            )
            return errors

        plugin_root = _plugin_root_in_clone(Path(tmpdir), source)
        if plugin_root is None:
            errors.append(
                f"  Plugin '{plugin['name']}': source.path escapes the repository root"
            )
            return errors
        if not plugin_root.is_dir():
            errors.append(
                f"  Plugin '{plugin['name']}': subdirectory "
                f"'{source_subdir(source)}' not found in the cloned repo"
            )
            return errors
        repo_path = plugin_root

        if strict:
            # Strict mode: plugin.json must exist in the repo
            plugin_json = repo_path / ".claude-plugin" / "plugin.json"
            if not plugin_json.exists():
                errors.append(
                    f"  Plugin '{plugin['name']}': missing .claude-plugin/plugin.json "
                    "(strict mode). Add plugin.json or set strict: false in registry.yaml"
                )
        # Check for at least one SKILL.md
        skills_dir_val = plugin.get("skills_dir", "skills")
        skills_dir = Path(skills_dir_val)
        resolved_skills_dir = (repo_path / skills_dir).resolve()
        if skills_dir.is_absolute() or not resolved_skills_dir.is_relative_to(repo_path.resolve()):
            errors.append(
                f"  Plugin '{plugin['name']}': invalid skills_dir '{skills_dir_val}' escapes the repository root"
            )
            return errors
        skill_locations = [
            resolved_skills_dir,
            repo_path / ".claude" / "skills",
            repo_path / "skills",
        ]
        found_skills = False
        for loc in skill_locations:
            if loc.exists() and list(loc.glob("*/SKILL.md")):
                found_skills = True
                break

        if not found_skills:
            errors.append(
                f"  Plugin '{plugin['name']}': no SKILL.md found in any skills directory"
            )

    return errors


def _iter_upstream_skill_files(plugin: dict, repo_path: Path) -> list[Path]:
    """SKILL.md files in a cloned plugin repo, from the first skills directory that has any.

    Mirrors the first-match lookup in validate_remote_plugin() rather than taking the union.
    A repo can ship its published skills in skills/ while also keeping its own tooling in
    .claude/skills/; unioning the two would report that tooling as missing from the registry.
    """
    root = repo_path.resolve()
    locations = [
        repo_path / plugin.get("skills_dir", "skills"),
        repo_path / ".claude" / "skills",
        repo_path / "skills",
    ]
    for location in locations:
        try:
            resolved = location.resolve()
        except OSError:
            continue
        if not resolved.is_relative_to(root) or not resolved.is_dir():
            continue
        found = sorted(resolved.glob("*/SKILL.md"))
        if found:
            return found
    return []


def check_skill_names_against_source(plugin: dict, repo_path: Path) -> tuple[list[str], list[str]]:
    """Compare registry skill names with the upstream SKILL.md frontmatter in a cloned repo.

    Returns (errors, warnings). A registry skill with no upstream SKILL.md is an error:
    the catalog publishes a slash command that resolves to nothing. Upstream skills the
    registry omits, and user-invocable disagreements, are warnings -- they misdescribe the
    plugin without inventing a command, and several are known upstream-side gaps.
    """
    from scripts.discover_skills import parse_frontmatter

    name = get_plugin_label(plugin)
    upstream: dict[str, bool] = {}
    for skill_md in _iter_upstream_skill_files(plugin, repo_path):
        try:
            frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        if not isinstance(frontmatter, dict):
            continue
        declared = frontmatter.get("name")
        skill_name = declared.strip() if isinstance(declared, str) and declared.strip() \
            else skill_md.parent.name
        # Absent user-invocable means the Claude Code default, which is true.
        upstream[skill_name] = frontmatter.get("user-invocable", True) is not False

    if not upstream:
        # validate_remote_plugin already reports "no SKILL.md found"; don't double-report.
        return [], []

    errors = []
    warnings = []
    registered = set()
    for skill in iter_skills(plugin):
        skill_name = skill.get("name")
        if not isinstance(skill_name, str):
            continue
        registered.add(skill_name)
        if skill_name not in upstream:
            errors.append(
                f"  Plugin '{name}' skill '{skill_name}': no upstream SKILL.md declares this name "
                f"(found: {', '.join(sorted(upstream)) or 'none'}). "
                "The catalog would publish a command that does not exist."
            )
            continue
        registry_invocable = skill.get("user-invocable", True) is not False
        if registry_invocable != upstream[skill_name]:
            warnings.append(
                f"  Plugin '{name}' skill '{skill_name}': registry says "
                f"user-invocable={registry_invocable}, upstream SKILL.md resolves to "
                f"{upstream[skill_name]}. Set user-invocable in the source SKILL.md to match."
            )

    # Only flag unlisted upstream skills for strict: false plugins. There the whole
    # skills_dir is installed, so anything missing from registry.yaml is a live command
    # with no documentation. A strict: true registry list is a curated subset by design.
    if plugin.get("strict", True) is False:
        unlisted = sorted(set(upstream) - registered)
        if unlisted:
            shown = ", ".join(unlisted[:5])
            more = f", +{len(unlisted) - 5} more" if len(unlisted) > 5 else ""
            warnings.append(
                f"  Plugin '{name}': {len(unlisted)} upstream skill(s) not listed in "
                f"registry.yaml ({shown}{more}). strict: false installs the whole "
                "skills_dir, so these are undocumented commands."
            )

    return errors, warnings


def diff_touched_plugins(registry: dict, base_ref: str) -> list[str] | None:
    """Plugin names whose registry entry differs from base_ref, or None if base is unreadable."""
    try:
        base_registry = load_registry_from_ref(base_ref)
    except (subprocess.CalledProcessError, RuntimeError, ValueError):
        return None
    base_by_name = {p.get("name"): p for p in base_registry.get("plugins", [])}
    return sorted(
        p.get("name")
        for p in registry.get("plugins", [])
        if base_by_name.get(p.get("name")) != p
    )


def check_codex_manifest(plugin: dict, plugin_root: Path) -> tuple[list[str], list[str]]:
    """Warn (never error) when a skill-bearing plugin's repo has no Codex manifest.

    Codex discovers a plugin's skills from that plugin's own .codex-plugin/plugin.json
    ``skills`` path. A plugin that declares skills but ships no such manifest installs
    with zero skills under Codex. That is an upstream repo property the registry cannot
    fix, so it is reported as a warning for the weekly sweep, never a blocking error.

    ``plugin_root`` is the plugin's root inside the clone (the subdir for git-subdir).
    """
    # A bundle installs its members, not skills of its own; a plugin that declares
    # no skills (e.g. an MCP-only plugin) has nothing to lose under Codex.
    if plugin.get("includes"):
        return [], []
    has_skills = bool(plugin.get("skills")) or bool(plugin.get("skill_count"))
    if not has_skills:
        return [], []
    if (plugin_root / ".codex-plugin" / "plugin.json").is_file():
        return [], []

    name = get_plugin_label(plugin)
    hint = ""
    if (plugin_root / ".claude-plugin" / "plugin.json").is_file():
        hint = (" (a .claude-plugin/plugin.json exists, but Codex is only confirmed to "
                "read the legacy .claude-plugin/marketplace.json, not a plugin manifest)")
    return [], [
        f"  Plugin '{name}': no .codex-plugin/plugin.json in source{hint}; its skills "
        "will not load under Codex until one is added upstream."
    ]


def _scope_plugins(registry: dict, diff_base: str | None) -> tuple[list[dict], str]:
    """Plugins to sweep, optionally narrowed to those whose entry changed since diff_base."""
    plugins = registry.get("plugins", [])
    if not diff_base:
        return plugins, "all"
    touched = diff_touched_plugins(registry, diff_base)
    if touched is None:
        print(f"WARNING: could not read registry.yaml from {diff_base}, "
              "checking every plugin", file=sys.stderr)
        return plugins, "all"
    names = set(touched)
    return [p for p in plugins if p.get("name") in names], f"touched since {diff_base}"


def run_on_clones(plugins: list[dict], per_plugin) -> tuple[list[str], list[str]]:
    """Clone each distinct (clone_url, ref) once and run per-plugin clone checks.

    ``per_plugin(plugin, plugin_root)`` returns (errors, warnings), aggregated across
    all plugins. Plugins that share a repo+ref (e.g. every git-subdir bundle member of
    one monorepo) are cloned a single time. A malformed source is skipped silently
    (validate_remote_plugin reports those); a failed clone or a missing subdirectory
    yields a warning for the affected plugin(s) — an upstream/transient condition, not
    a registry error — mirroring the existing skill-name sweep.
    """
    groups: dict[tuple[str, str], list[dict]] = {}
    errors: list[str] = []
    warnings: list[str] = []

    for plugin in plugins:
        source = plugin.get("source") or {}
        if source.get("type") not in GIT_CLONEABLE_TYPES:
            continue
        try:
            clone_url = source_clone_url(source)
            ref = normalize_git_ref(source.get("ref", "main"))
        except (ValueError, KeyError):
            continue
        groups.setdefault((clone_url, ref), []).append(plugin)

    for (clone_url, ref), members in groups.items():
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                result = shallow_clone(clone_url, ref, tmpdir)
                clone_ok = result.returncode == 0
            except RuntimeError as exc:
                for plugin in members:
                    warnings.append(
                        f"  Plugin '{get_plugin_label(plugin)}': could not clone to run "
                        f"upstream checks: {redact_url(str(exc))}"
                    )
                continue
            if not clone_ok:
                for plugin in members:
                    warnings.append(
                        f"  Plugin '{get_plugin_label(plugin)}': could not clone "
                        f"{redact_url(clone_url)} (ref={ref}) to run upstream checks"
                    )
                continue
            for plugin in members:
                plugin_root = _plugin_root_in_clone(Path(tmpdir), plugin["source"])
                if plugin_root is None or not plugin_root.is_dir():
                    warnings.append(
                        f"  Plugin '{get_plugin_label(plugin)}': subdirectory "
                        f"'{source_subdir(plugin['source'])}' not found in the cloned repo"
                    )
                    continue
                e, w = per_plugin(plugin, plugin_root)
                errors.extend(e)
                warnings.extend(w)

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", default="registry.yaml")
    parser.add_argument("--schema", default="schema/registry.schema.json")
    parser.add_argument("--check-sources", action="store_true",
                        help="Check that GitHub repos are accessible")
    parser.add_argument("--diff", metavar="BASE_REF",
                        help="Show plugins added since BASE_REF")
    parser.add_argument("--validate-remote-plugins", action="store_true",
                        help="Clone and validate plugin repos")
    parser.add_argument("--check-skill-names", action="store_true",
                        help="Clone plugin repos and check registry skill names against "
                             "upstream SKILL.md frontmatter (scoped to plugins touched "
                             "since --diff-base, if given)")
    parser.add_argument("--check-codex-manifests", action="store_true",
                        help="Clone plugin repos and warn (never fail) about skill-bearing "
                             "plugins missing a .codex-plugin/plugin.json, whose skills will "
                             "not load under Codex (scoped to --diff-base, if given)")
    parser.add_argument("--staged", action="store_true",
                        help="Require contracts for skills changed between HEAD and staged registry.yaml")
    parser.add_argument("--diff-base", metavar="REF",
                        help="Require contracts for skills changed between REF and the current registry file")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    schema = load_schema(args.schema)
    all_errors = []

    # Schema validation
    print("Validating schema...")
    errors = validate_schema(registry, schema)
    all_errors.extend(errors)
    if errors:
        print(f"  FAIL: {len(errors)} schema error(s)")
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print("  OK")

    # Duplicate check
    print("Checking for duplicates...")
    errors = check_duplicates(registry)
    all_errors.extend(errors)
    if errors:
        print(f"  FAIL: {len(errors)} duplicate(s)")
        for e in errors:
            print(e)
    else:
        print("  OK")

    # Category check
    print("Checking categories...")
    errors = check_categories(registry)
    all_errors.extend(errors)
    if errors:
        print(f"  FAIL: {len(errors)} category error(s)")
        for e in errors:
            print(e)
    else:
        print("  OK")

    # Bundle (meta-plugin) check
    print("Checking bundles...")
    errors = check_bundles(registry)
    all_errors.extend(errors)
    if errors:
        print(f"  FAIL: {len(errors)} bundle error(s)")
        for e in errors:
            print(e)
    else:
        print("  OK")

    # Strict/skills_dir consistency
    print("Checking strict/skills_dir consistency...")
    errors = check_strict_consistency(registry)
    all_errors.extend(errors)
    if errors:
        print(f"  FAIL: {len(errors)} consistency error(s)")
        for e in errors:
            print(e)
    else:
        print("  OK")

    # Skill contract semantics (required for touched skills when --staged / --diff-base)
    print("Checking skill contracts...")
    required_skills, skill_select_errors = select_required_skills(args, registry)
    errors = check_skill_contracts(registry, required_skills)
    contract_errors = [*skill_select_errors, *errors]
    all_errors.extend(contract_errors)
    if contract_errors:
        print(f"  FAIL: {len(contract_errors)} contract error(s)")
        for e in contract_errors:
            print(e)
    else:
        print("  OK")

    # Source accessibility
    if args.check_sources:
        print("Checking sources...")
        errors = check_sources(registry)
        all_errors.extend(errors)
        if errors:
            print(f"  FAIL: {len(errors)} source error(s)")
        else:
            print("  OK")

    # Diff
    new_plugins = []
    if args.diff:
        new_plugins = diff_plugins(registry, args.diff)
        if new_plugins:
            print(f"New plugins since {args.diff}: {', '.join(new_plugins)}")
        else:
            print(f"No new plugins since {args.diff}")

    # Remote validation
    if args.validate_remote_plugins:
        plugins_to_check = registry.get("plugins", [])
        if args.diff:
            new_names = set(new_plugins)
            plugins_to_check = [p for p in plugins_to_check if p["name"] in new_names]

        print(f"Validating {len(plugins_to_check)} remote plugin(s)...")
        for plugin in plugins_to_check:
            print(f"  Checking {plugin['name']}...")
            errors = validate_remote_plugin(plugin)
            all_errors.extend(errors)
            if errors:
                for e in errors:
                    print(e)
            else:
                print("    OK")

    # Upstream clone-based sweeps: skill-name drift and/or Codex-manifest presence.
    # Both clone the same repos, so when both are requested we clone each repo once
    # (git-subdir bundle members of one monorepo share a single clone regardless).
    if args.check_skill_names or args.check_codex_manifests:
        plugins_to_check, scope = _scope_plugins(registry, args.diff_base)

        clone_checks = []
        if args.check_skill_names:
            clone_checks.append(check_skill_names_against_source)
        if args.check_codex_manifests:
            clone_checks.append(check_codex_manifest)

        labels = " + ".join(
            label for label, enabled in (
                ("skill names", args.check_skill_names),
                ("Codex manifests", args.check_codex_manifests),
            ) if enabled
        )
        print(f"Checking {labels} against source ({len(plugins_to_check)} plugin(s), {scope})...")

        def _combined(plugin: dict, plugin_root: Path) -> tuple[list[str], list[str]]:
            errs: list[str] = []
            warns: list[str] = []
            for check in clone_checks:
                e, w = check(plugin, plugin_root)
                errs.extend(e)
                warns.extend(w)
            return errs, warns

        sweep_errors, sweep_warnings = run_on_clones(plugins_to_check, _combined)
        for w in sweep_warnings:
            print(f"  WARNING:{w.lstrip(' ')}")
        all_errors.extend(sweep_errors)
        if sweep_errors:
            print(f"  FAIL: {len(sweep_errors)} error(s)")
            for e in sweep_errors:
                print(e)
        else:
            print("  OK")

    # Summary
    print()
    plugin_count = len(registry.get("plugins", []))
    # Count each skill once: leaf plugins by their skill_count (or listed
    # skills); bundles are excluded since their members are counted individually.
    skill_count = sum(
        p.get("skill_count", len(p.get("skills", [])))
        for p in registry.get("plugins", [])
        if not p.get("includes")
    )
    print(f"Registry: {plugin_count} plugin(s), {skill_count} skill(s)")

    if all_errors:
        print(f"\nFAILED: {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("\nPASSED")


if __name__ == "__main__":
    main()
