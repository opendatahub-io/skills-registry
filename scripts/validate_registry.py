#!/usr/bin/env python3
"""Validate registry.yaml against the JSON Schema and check plugin sources.

Usage:
    python3 scripts/validate_registry.py                        # Schema validation only
    python3 scripts/validate_registry.py --check-sources        # Also check GitHub repos exist
    python3 scripts/validate_registry.py --diff origin/main     # Detect newly added plugins
    python3 scripts/validate_registry.py --validate-remote-plugins  # Clone and validate new plugins
    python3 scripts/validate_registry.py --staged               # Require contracts for skills changed vs HEAD (staged registry)
    python3 scripts/validate_registry.py --diff-base REF        # Require contracts for skills changed since REF
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
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.registry_contracts import (  # noqa: E402
    CANONICAL_FUNCTIONS,
    CANONICAL_METRICS,
    SkillKey,
    detect_touched_skills,
    iter_plugins,
    iter_skills,
    load_registry_from_ref,
    load_staged_registry,
    normalize_git_ref,
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
    """Check that GitHub repos are accessible via the GitHub API."""
    errors = []
    for plugin in registry.get("plugins", []):
        source = plugin.get("source")
        if not source or source.get("type") != "github":
            continue
        repo = source.get("repo")
        if not repo:
            continue
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}", "--silent"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            errors.append(f"  Plugin '{plugin['name']}': repo '{repo}' not accessible")
        else:
            print(f"  OK: {repo}")
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


def validate_remote_plugin(plugin: dict) -> list[str]:
    """Clone a plugin repo and validate its structure."""
    errors = []
    source = plugin.get("source")
    if not source or source.get("type") != "github":
        return errors

    repo = source["repo"]
    try:
        ref = normalize_git_ref(source.get("ref", "main"))
    except ValueError:
        errors.append(f"  Plugin '{plugin['name']}': invalid source.ref")
        return errors
    strict = plugin.get("strict", True)

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_url = f"https://github.com/{repo}.git"
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", ref, "--", clone_url, tmpdir],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            errors.append(f"  Plugin '{plugin['name']}': failed to clone {clone_url} (ref={ref})")
            return errors

        repo_path = Path(tmpdir)

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

    # Summary
    print()
    plugin_count = len(registry.get("plugins", []))
    skill_count = sum(len(p.get("skills", [])) for p in registry.get("plugins", []))
    print(f"Registry: {plugin_count} plugin(s), {skill_count} skill(s)")

    if all_errors:
        print(f"\nFAILED: {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("\nPASSED")


if __name__ == "__main__":
    main()
