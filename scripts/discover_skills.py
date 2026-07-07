#!/usr/bin/env python3
"""Discover skills from a plugin's source repo and populate registry.yaml.

Fetches SKILL.md frontmatter from GitHub, formats the skills list, and
writes it into registry.yaml surgically (no yaml.dump, preserves formatting).

Usage:
    python3 scripts/discover_skills.py --plugin docs-skills
    python3 scripts/discover_skills.py --plugin docs-skills --dry-run
"""

import argparse
import json
import os
import re
import sys
import tempfile
import textwrap
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT_STR = str(_SCRIPT_DIR.parent)
sys.path[:] = [entry for entry in sys.path if entry != _REPO_ROOT_STR]
sys.path.insert(0, _REPO_ROOT_STR)

from scripts.registry_contracts import redact_url, source_clone_url, shallow_clone  # noqa: E402


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def github_get(url: str) -> bytes:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def parse_frontmatter(content: str) -> dict:
    content = content.lstrip()
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(content[3:end]) or {}
    except yaml.YAMLError:
        return {}


def discover_remote_skills(repo: str, ref: str = "main") -> list[dict]:
    tree_url = f"https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1"
    tree_data = json.loads(github_get(tree_url))

    if tree_data.get("truncated"):
        print(f"  Warning: tree for {repo} was truncated, some skills may be missed",
              file=sys.stderr)

    skill_entries = []
    for item in tree_data.get("tree", []):
        if item["type"] == "blob" and item["path"].endswith("/SKILL.md"):
            parent = item["path"].rsplit("/", 1)[0]
            skill_name = parent.rsplit("/", 1)[-1]
            skill_entries.append((skill_name, parent, item["path"]))

    if not skill_entries:
        return []

    def fetch_one(entry):
        skill_name, _parent_path, full_path = entry
        raw_url = f"https://raw.githubusercontent.com/{repo}/{ref}/{full_path}"
        try:
            content = github_get(raw_url).decode("utf-8", errors="replace")
            fm = parse_frontmatter(content)
            return {
                "name": fm.get("name", skill_name),
                "description": fm.get("description", ""),
                "user-invocable": fm.get("user-invocable", True),
            }
        except Exception as exc:
            print(f"  Warning: failed to fetch {full_path}: {exc}", file=sys.stderr)
            return {
                "name": skill_name,
                "description": "",
                "user-invocable": True,
            }

    with ThreadPoolExecutor(max_workers=8) as pool:
        skills = list(pool.map(fetch_one, sorted(skill_entries)))

    return sorted(skills, key=lambda s: s["name"])


def discover_git_skills(clone_url: str, ref: str = "main") -> list[dict]:
    """Discover skills by cloning a git repo and walking for SKILL.md files.

    Used for non-GitHub ``type: git`` sources, where the GitHub tree/raw APIs
    are unavailable.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            result = shallow_clone(clone_url, ref, tmpdir)
        except RuntimeError as exc:
            print(f"  ERROR: {redact_url(str(exc))}", file=sys.stderr)
            return []
        if result.returncode != 0:
            print(f"  ERROR: clone failed for {redact_url(clone_url)}: "
                  f"{redact_url(result.stderr.strip())}",
                  file=sys.stderr)
            return []

        skills = []
        for skill_md in Path(tmpdir).rglob("SKILL.md"):
            content = skill_md.read_text(encoding="utf-8", errors="replace")
            fm = parse_frontmatter(content)
            skills.append({
                "name": fm.get("name", skill_md.parent.name),
                "description": fm.get("description", ""),
                "user-invocable": fm.get("user-invocable", True),
            })
        return sorted(skills, key=lambda s: s["name"])


def format_skills_yaml(skills: list[dict]) -> str:
    lines = []
    for skill in skills:
        lines.append(f"      - name: {skill['name']}")
        desc = skill.get("description", "").strip()
        if desc:
            if len(desc) <= 80:
                lines.append(f"        description: {desc}")
            else:
                lines.append("        description: >")
                for wrapped in textwrap.wrap(desc, width=90):
                    lines.append(f"          {wrapped}")
        invocable = skill.get("user-invocable", True)
        if not invocable:
            lines.append("        user-invocable: false")
    return "\n".join(lines)


def update_skills_in_file(path: str, plugin_name: str, skills_yaml: str):
    with open(path) as f:
        content = f.read()

    escaped_name = re.escape(plugin_name)
    plugin_pattern = re.compile(
        rf'^(  - name: {escaped_name}\b.*?)(?=^  - name: |\Z)',
        re.MULTILINE | re.DOTALL,
    )

    match = plugin_pattern.search(content)
    if not match:
        print(f"ERROR: plugin '{plugin_name}' not found in {path}", file=sys.stderr)
        sys.exit(1)

    plugin_text = match.group(1)
    skills_block_pattern = re.compile(
        r'^(    skills:\s*\n)((?:      - .*\n|        .*\n)*)',
        re.MULTILINE,
    )
    skills_match = skills_block_pattern.search(plugin_text)

    if skills_match:
        old_block = skills_match.group(0)
        new_block = "    skills:\n" + skills_yaml + "\n"
        new_plugin_text = plugin_text.replace(old_block, new_block, 1)
    else:
        empty_pattern = re.compile(r'^    skills:\s*\[\s*\]\s*$', re.MULTILINE)
        empty_match = empty_pattern.search(plugin_text)
        if empty_match:
            new_plugin_text = plugin_text.replace(
                empty_match.group(0),
                "    skills:\n" + skills_yaml,
                1,
            )
        else:
            insert_before = re.search(r'^    harnesses:', plugin_text, re.MULTILINE)
            if insert_before:
                pos = insert_before.start()
                new_plugin_text = (
                    plugin_text[:pos]
                    + "    skills:\n" + skills_yaml + "\n"
                    + plugin_text[pos:]
                )
            else:
                new_plugin_text = plugin_text.rstrip("\n") + "\n    skills:\n" + skills_yaml + "\n"

    content = content[:match.start()] + new_plugin_text + content[match.end():]

    with open(path, "w") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--plugin", required=True, help="Plugin name in registry.yaml")
    parser.add_argument("--registry", default="registry.yaml", help="Registry file path")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show discovered skills without modifying files")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    plugin = None
    for p in registry.get("plugins", []):
        if p.get("name") == args.plugin:
            plugin = p
            break

    if plugin is None:
        print(f"ERROR: plugin '{args.plugin}' not found in {args.registry}", file=sys.stderr)
        sys.exit(1)

    source = plugin.get("source") or {}
    source_type = source.get("type")
    ref = source.get("ref", "main")

    if source_type == "github":
        repo = source.get("repo")
        if not repo:
            print(f"ERROR: plugin '{args.plugin}' has no source.repo", file=sys.stderr)
            sys.exit(1)
        print(f"Discovering skills for {args.plugin} from {repo}@{ref}...")
        skills = discover_remote_skills(repo, ref)
    elif source_type == "git":
        try:
            clone_url = source_clone_url(source)
        except (ValueError, KeyError):
            print(f"ERROR: plugin '{args.plugin}' has an invalid git source", file=sys.stderr)
            sys.exit(1)
        print(f"Discovering skills for {args.plugin} from {redact_url(clone_url)}@{ref}...")
        skills = discover_git_skills(clone_url, ref)
    else:
        print(
            f"ERROR: plugin '{args.plugin}' source type {source_type!r} is not "
            "supported for skill discovery (expected 'github' or 'git')",
            file=sys.stderr,
        )
        sys.exit(1)
    if not skills:
        print("  No skills found.")
        return

    print(f"  Found {len(skills)} skill(s):")
    for s in skills:
        inv = "" if s.get("user-invocable", True) else " (internal)"
        print(f"    {s['name']}{inv}")

    if args.dry_run:
        print(f"\nDry run — {len(skills)} skill(s) discovered, no files modified.")
        return

    skills_yaml = format_skills_yaml(skills)
    update_skills_in_file(args.registry, args.plugin, skills_yaml)
    print(f"\nUpdated {args.registry} with {len(skills)} skill(s) for {args.plugin}")


if __name__ == "__main__":
    main()
