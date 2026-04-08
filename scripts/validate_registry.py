#!/usr/bin/env python3
"""Validate registry.yaml against the JSON Schema and check plugin sources.

Usage:
    python3 scripts/validate_registry.py                        # Schema validation only
    python3 scripts/validate_registry.py --check-sources        # Also check GitHub repos exist
    python3 scripts/validate_registry.py --diff origin/main     # Detect newly added plugins
    python3 scripts/validate_registry.py --validate-remote-plugins  # Clone and validate new plugins
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

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
    result = subprocess.run(
        ["git", "show", "--", f"{base_ref}:registry.yaml"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"WARNING: could not read registry.yaml from {base_ref}, treating all as new",
              file=sys.stderr)
        return [p["name"] for p in registry.get("plugins", [])]

    base_registry = yaml.safe_load(result.stdout)
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
    ref = source.get("ref", "main")
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
                    f"(strict mode). Add plugin.json or set strict: false in registry.yaml"
                )
        # Check for at least one SKILL.md
        skills_dir = plugin.get("skills_dir", "skills")
        skill_locations = [
            repo_path / skills_dir,
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


def main():
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
