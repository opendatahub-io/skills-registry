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
import subprocess
import sys

import yaml


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def save_registry(registry: dict, path: str = "registry.yaml"):
    with open(path, "w") as f:
        yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def fetch_remote_version(repo: str, ref: str = "main") -> str | None:
    """Fetch version from remote plugin.json via GitHub API."""
    result = subprocess.run(
        ["gh", "api",
         f"repos/{repo}/contents/.claude-plugin/plugin.json?ref={ref}",
         "--jq", ".content"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None

    try:
        content = base64.b64decode(result.stdout.strip()).decode()
        data = json.loads(content)
        return data.get("version")
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
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
        source = plugin["source"]
        if source["type"] != "github":
            continue

        # Only check strict-mode plugins (they have their own plugin.json)
        if plugin.get("strict", True) is False:
            continue

        repo = source["repo"]
        current = plugin.get("version", "0.0.0")
        remote = fetch_remote_version(repo, source.get("ref", "main"))

        if remote is None:
            print(f"  SKIP: {plugin['name']} (could not fetch remote version)")
            continue

        if remote != current:
            print(f"  UPDATE: {plugin['name']} {current} -> {remote}")
            updates.append((plugin, remote))
        else:
            print(f"  OK: {plugin['name']} {current}")

    if not updates:
        print("\nAll plugins up to date.")
        return

    if args.dry_run:
        print(f"\n{len(updates)} update(s) found (dry run, no changes made)")
        return

    # Apply updates
    for plugin, new_version in updates:
        plugin["version"] = new_version

    save_registry(registry, args.registry)
    print(f"\nUpdated {len(updates)} plugin(s) in {args.registry}")

    # Regenerate marketplace.json
    result = subprocess.run(
        [sys.executable, "scripts/sync_marketplace.py", "--registry", args.registry],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f"WARNING: failed to regenerate marketplace.json: {result.stderr}",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
