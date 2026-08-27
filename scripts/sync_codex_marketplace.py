#!/usr/bin/env python3
"""Generate .agents/plugins/marketplace.json from registry.yaml.

This script projects the universal registry format into OpenAI Codex's
native marketplace.json format (developers.openai.com/codex/plugins/build.md).

It is the Codex counterpart to scripts/sync_marketplace.py, which emits the
Claude Code native .claude-plugin/marketplace.json. Both files are generated
from the same registry.yaml, but the Codex projection differs on almost every
mapping, so this generator is intentionally standalone (like the other sibling
generators, it defines its own load_registry rather than importing one):

  * top level is {name, interface?, plugins[]} — no owner/metadata
  * each entry is exactly {name, source, policy, category}
  * github sources become source:"url" with a full .git clone URL
  * per-entry skills/strict/agents are dropped (Codex discovers skills from
    each plugin's own .codex-plugin/plugin.json)

Usage:
    python3 scripts/sync_codex_marketplace.py [--registry registry.yaml] [--output .agents/plugins/marketplace.json]
"""

import argparse
import json
from pathlib import Path

import yaml


# Default Codex per-entry policy. The docs say to "always include"
# policy.installation and policy.authentication, so both are emitted on every
# entry. "AVAILABLE" keeps plugins installable but opt-in (never force-installed
# on every team member); "ON_INSTALL" is the spec default and the only value
# shown in the documented example. policy.products is omitted unless a plugin
# explicitly requests product gating via codex_policy.products.
DEFAULT_POLICY = {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def _rel_path(name: str, path: str) -> str:
    """Normalize a source path to a ``./``-prefixed, root-relative form.

    Rejects absolute paths and any parent-directory (``..``) component so a
    source cannot escape the marketplace/repository root (CWE-22). Codex resolves
    ``local``/``git-subdir`` paths from that root, so ``..`` must not leak through.
    """
    normalized = path.replace("\\", "/")
    if normalized.startswith("/") or (len(path) > 1 and path[1] == ":"):
        raise ValueError(f"{name!r}: source path must be relative, got {path!r}")
    if ".." in normalized.split("/"):
        raise ValueError(f"{name!r}: source path must not contain '..': {path!r}")
    return path if path.startswith("./") else "./" + path


def _map_source(name: str, source: dict) -> dict:
    """Map a registry source object to a Codex source object.

    Every Codex source nests a `source` string key inside the source object.
    ref/sha are carried through for every git-backed type.
    """
    stype = source["type"]

    if stype == "github":
        # The Codex marketplace FILE documents remote git-root plugins with
        # source:"url" + a full clone URL (owner/repo shorthand is CLI-only),
        # so derive the .git clone URL rather than emitting source:"github".
        mapped = {"source": "url", "url": f"https://github.com/{source['repo']}.git"}
        if "ref" in source:
            mapped["ref"] = source["ref"]
        if "sha" in source:
            mapped["sha"] = source["sha"]
        return mapped

    if stype == "git":
        mapped = {"source": "url", "url": source["url"]}
        if "ref" in source:
            mapped["ref"] = source["ref"]
        if "sha" in source:
            mapped["sha"] = source["sha"]
        return mapped

    if stype == "git-subdir":
        path = _rel_path(name, source["path"])
        mapped = {"source": "git-subdir", "url": source["url"], "path": path}
        if "ref" in source:
            mapped["ref"] = source["ref"]
        if "sha" in source:
            mapped["sha"] = source["sha"]
        return mapped

    if stype == "npm":
        # Forward-looking: the registry schema does not yet define
        # package/version/registry on npm sources, so this path is unreachable
        # today. package is required by Codex when present.
        if "package" not in source:
            raise ValueError(
                f"{name!r}: npm source requires a 'package' field for Codex"
            )
        mapped = {"source": "npm", "package": source["package"]}
        if "version" in source:
            mapped["version"] = source["version"]
        if "registry" in source:
            mapped["registry"] = source["registry"]
        return mapped

    if stype == "local":
        return {"source": "local", "path": _rel_path(name, source["path"])}

    raise ValueError(f"{name!r}: unknown source type {stype!r}")


def _map_policy(plugin: dict) -> dict:
    """Build the per-entry policy, applying any per-plugin codex_policy override."""
    policy = dict(DEFAULT_POLICY)
    override = plugin.get("codex_policy") or {}
    for key in ("installation", "authentication"):
        if key in override:
            policy[key] = override[key]
    # products is emitted only when a plugin explicitly opts into gating.
    if "products" in override:
        policy["products"] = override["products"]
    return policy


def _map_category(plugin: dict, categories: dict) -> str:
    """Map the registry category KEY to its human display name (Codex bucket)."""
    key = plugin.get("category")
    meta = categories.get(key) if key else None
    if meta and "name" in meta:
        return meta["name"]
    # Codex asks for a display bucket on every entry ("always include category").
    # validate_registry.py already guarantees a defined key today; fall back to
    # the raw key, else a generic bucket, so we never emit a null category.
    return key or "Productivity"


def plugin_to_marketplace_entry(plugin: dict, categories: dict) -> dict:
    """Convert a registry plugin entry to a Codex marketplace plugin entry.

    A Codex entry is minimal: exactly {name, source, policy, category}. The
    Claude direct fields (description/version/author/homepage/repository/
    license/keywords) and the per-entry skills/strict/agents projections are
    intentionally dropped — Codex reads those from each plugin's own manifest.
    """
    return {
        "name": plugin["name"],
        "source": _map_source(plugin["name"], plugin["source"]),
        "policy": _map_policy(plugin),
        "category": _map_category(plugin, categories),
    }


def generate_marketplace(registry: dict) -> dict:
    """Generate Codex marketplace.json content from registry data."""
    marketplace = {
        "name": registry["name"],
        "plugins": [],
    }

    # interface.displayName is Codex's optional marketplace title (its
    # replacement for Claude's top-level metadata.description). Emit it only
    # when an explicit top-level `display_name` is set; do NOT fall back to the
    # slug `name`, which would surface an unpolished title in the ChatGPT app.
    display_name = registry.get("display_name")
    if display_name:
        marketplace["interface"] = {"displayName": display_name}

    categories = registry.get("categories", {})

    # Preserve registry.yaml plugin order — array order is Codex render order.
    for plugin in registry.get("plugins", []):
        entry = plugin_to_marketplace_entry(plugin, categories)
        marketplace["plugins"].append(entry)

    return marketplace


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", default="registry.yaml",
                        help="Path to registry.yaml (default: registry.yaml)")
    parser.add_argument("--output", default=".agents/plugins/marketplace.json",
                        help="Output path (default: .agents/plugins/marketplace.json)")
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
