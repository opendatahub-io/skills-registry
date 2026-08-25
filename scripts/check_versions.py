#!/usr/bin/env python3
"""Check for version updates in registered plugin repositories.

For each plugin with a GitHub source, fetches the remote plugin.json
and compares the version against registry.yaml. If updates are found,
updates registry.yaml and regenerates marketplace.json.

Usage:
    python3 scripts/check_versions.py [--registry registry.yaml] [--dry-run]
"""

import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

import yaml

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent
_REPO_ROOT_STR = str(_REPO_ROOT)
sys.path[:] = [entry for entry in sys.path if entry != _REPO_ROOT_STR]
sys.path.insert(0, _REPO_ROOT_STR)

from scripts.registry_contracts import GIT_CLONE_TYPES, source_clone_url, normalize_git_ref, shallow_clone  # noqa: E402


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def update_version_in_file(path: str, updates: list[tuple[dict, str]]):
    """Replace version strings in-place without reformatting the file."""
    with open(path) as f:
        content = f.read()
    for plugin, new_version in updates:
        name = re.escape(plugin["name"])
        old_version = re.escape(plugin["version"])
        pattern = rf'(name:\s*{name}\b.*?version:\s*)"?{old_version}"?'
        content = re.sub(pattern, rf'\g<1>"{new_version}"', content, count=1, flags=re.DOTALL)
    with open(path, "w") as f:
        f.write(content)


def fetch_remote_version(repo: str, ref: str = "main") -> str | None:
    """Fetch version from remote plugin.json via GitHub API."""
    gh_bin = shutil.which("gh")
    if not gh_bin:
        return None
    result = subprocess.run(
        [gh_bin, "api",
         f"repos/{repo}/contents/.claude-plugin/plugin.json?ref={quote(ref, safe='')}",
         "--jq", ".content"],
        capture_output=True, text=True,
        timeout=30,
    )
    if result.returncode != 0:
        return None

    try:
        content = base64.b64decode(result.stdout.strip()).decode()
        data = json.loads(content)
        return data.get("version")
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return None


def fetch_remote_version_via_clone(clone_url: str, ref: str = "main") -> str | None:
    """Fetch version from remote plugin.json via shallow clone."""
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            result = shallow_clone(clone_url, ref, tmpdir)
        except RuntimeError:
            return None
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


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", default="registry.yaml")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show updates without modifying files")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    updates = []

    for plugin in registry.get("plugins", []):
        source = plugin.get("source") or {}
        source_type = source.get("type")
        if source_type not in GIT_CLONE_TYPES:
            continue

        # Only check strict-mode plugins (they have their own plugin.json)
        if plugin.get("strict", True) is False:
            continue

        name = plugin.get("name", "<unknown>")
        current = plugin.get("version", "0.0.0")
        if source_type == "github":
            repo = source.get("repo")
            if not repo:
                print(f"  SKIP: {name} (missing source.repo)")
                continue
            remote = fetch_remote_version(repo, source.get("ref", "main"))
        else:
            try:
                clone_url = source_clone_url(source)
                ref = normalize_git_ref(source.get("ref", "main"))
            except (ValueError, KeyError):
                print(f"  SKIP: {name} (invalid source configuration)")
                continue
            remote = fetch_remote_version_via_clone(clone_url, ref)
        if remote is None:
            print(f"  SKIP: {name} (could not fetch remote version)")
            continue

        if remote != current:
            print(f"  UPDATE: {name} {current} -> {remote}")
            updates.append((plugin, remote))
        else:
            print(f"  OK: {name} {current}")

    if not updates:
        print("\nAll plugins up to date.")
        return

    if args.dry_run:
        print(f"\n{len(updates)} update(s) found (dry run, no changes made)")
        return

    # Apply updates (surgical text replacement to preserve formatting)
    update_version_in_file(args.registry, updates)
    print(f"\nUpdated {len(updates)} plugin(s) in {args.registry}")

    # Regenerate marketplace.json
    result = subprocess.run(
        [sys.executable, "scripts/sync_marketplace.py", "--registry", args.registry],
        capture_output=True, text=True,
        timeout=60,
    )
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f"WARNING: failed to regenerate marketplace.json: {result.stderr}",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
