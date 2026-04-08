#!/usr/bin/env python3
"""Generate .claude-plugin/marketplace.json from registry.yaml.

This script projects the universal registry format into Claude Code's
native marketplace.json format, mapping source types and dropping fields
that marketplace.json does not support.

Usage:
    python3 scripts/sync_marketplace.py [--registry registry.yaml] [--output .claude-plugin/marketplace.json]
"""

import argparse
import json
from pathlib import Path

import yaml


# Fields from registry.yaml plugin entries that map directly to marketplace.json
DIRECT_FIELDS = {
    "name", "description", "version", "author", "homepage",
    "repository", "license", "category",
}


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def plugin_to_marketplace_entry(plugin: dict) -> dict:
    """Convert a registry plugin entry to a marketplace plugin entry."""
    entry = {}

    # Copy direct fields
    for field in DIRECT_FIELDS:
        if field in plugin:
            entry[field] = plugin[field]

    # Map tags to keywords (marketplace uses "keywords")
    if "tags" in plugin:
        entry["keywords"] = plugin["tags"]

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

    # Handle strict: false plugins
    if plugin.get("strict") is False:
        entry["strict"] = False
        if "skills_dir" in plugin:
            skills_dir = plugin["skills_dir"]
            if not skills_dir.startswith("./"):
                skills_dir = "./" + skills_dir
            entry["skills"] = [skills_dir]

    return entry


def generate_marketplace(registry: dict) -> dict:
    """Generate marketplace.json content from registry data."""
    marketplace = {
        "name": registry["name"],
        "owner": registry["owner"],
        "plugins": [],
    }

    if "description" in registry:
        marketplace["metadata"] = {
            "description": registry["description"],
        }

    for plugin in registry.get("plugins", []):
        entry = plugin_to_marketplace_entry(plugin)
        marketplace["plugins"].append(entry)

    return marketplace


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", default="registry.yaml",
                        help="Path to registry.yaml (default: registry.yaml)")
    parser.add_argument("--output", default=".claude-plugin/marketplace.json",
                        help="Output path (default: .claude-plugin/marketplace.json)")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    marketplace = generate_marketplace(registry)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(marketplace, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Generated {output_path} with {len(marketplace['plugins'])} plugin(s)")


if __name__ == "__main__":
    main()
