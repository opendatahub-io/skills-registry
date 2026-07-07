from __future__ import annotations

import re as _re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

CONTRACT_VERSION = "canonical-skill-v1"
SKILL_LINTER_VERSION = "0.1.4"
GIT_READ_TIMEOUT_SECONDS = 30
CANONICAL_FUNCTION_DOCS = {
    "plan": "Choose an approach, sequence, or strategy before execution.",
    "retrieve": "Locate and return source material, facts, or artifacts needed for later work.",
    "analyze": "Interpret inputs to extract structure, meaning, or implications.",
    "review": "Assess an artifact against expectations and identify issues, risks, or fit.",
    "generate": "Produce a new artifact for the user or another tool to consume.",
    "transform": "Rewrite or convert existing input into a different form while preserving intent.",
    "verify": "Check whether a claim, artifact, or result satisfies explicit criteria.",
    "execute": "Carry out a bounded operational task in tools, CLIs, or external systems.",
    "orchestrate": "Coordinate multiple steps, tools, or subagents into a larger workflow.",
}
CANONICAL_METRIC_DOCS = {
    "task_success": {
        "summary": "Whether the skill completes the intended job correctly for the task.",
        "measure_guidance": "Prefer deterministic or verifier-backed checks; use judge only as a fallback.",
    },
    "tool_correctness": {
        "summary": "Whether chosen tools and tool calls are valid and appropriate.",
        "measure_guidance": "Usually deterministic or verifier-backed from tool traces and outcomes.",
    },
    "argument_correctness": {
        "summary": "Whether tool inputs, flags, and parameters are correct.",
        "measure_guidance": "Usually deterministic or verifier-backed from arguments and downstream results.",
    },
    "evidence_completeness": {
        "summary": "Whether claims and verdicts are backed by enough concrete evidence.",
        "measure_guidance": "Use verifier-backed checks when evidence can be counted; otherwise use a rubric-backed judge.",
    },
    "step_efficiency": {
        "summary": "Whether the workflow uses a reasonable number of steps for the task.",
        "measure_guidance": "Deterministic only; count steps against an explicit budget or baseline.",
    },
    "latency": {
        "summary": "How quickly the skill produces the final usable result.",
        "measure_guidance": "Deterministic only; measure elapsed wall-clock time for the user-visible outcome.",
    },
    "token_efficiency": {
        "summary": "How economically the skill uses model tokens.",
        "measure_guidance": "Deterministic only; measure prompt/completion token consumption.",
    },
    "context_footprint": {
        "summary": "How much context the skill requires to do the job reliably.",
        "measure_guidance": "Deterministic only; measure required files, tokens, or supporting artifacts.",
    },
    "output_quality": {
        "summary": "Human-judged quality of the final artifact when deterministic checks are insufficient.",
        "measure_guidance": "Judge only; always pair it with a stable rubric_ref and, when available, calibration data.",
    },
}
MEASURE_DOCS = {
    "deterministic": "Use when a direct oracle or exact check can score the metric consistently.",
    "verifier_backed": "Use when a programmatic verifier can judge success, but not by simple exact match.",
    "judge": "Use rubric-based human or LLM evaluation only when deterministic checks are insufficient.",
}
CANONICAL_FUNCTIONS = frozenset(CANONICAL_FUNCTION_DOCS)
CANONICAL_METRICS = frozenset(CANONICAL_METRIC_DOCS)
PLUGIN_FIELDS_THAT_TOUCH_ALL_SKILLS = {"source", "strict", "skills_dir"}

_SCHEME_RE = _re.compile(r"^https?://")
GIT_CLONE_TYPES = frozenset({"github", "git"})

# Strip user[:token]@ credentials from any URL in the given text before logging.
# Applies to both the URL we hold and URLs that git echoes back in stderr /
# RuntimeError messages. Prevents credential leaks in logs (CWE-532).
_CREDENTIAL_URL_RE = _re.compile(r"(https?://)[^/@\s]*@")


def redact_url(text: str) -> str:
    """Replace `user[:token]@` in any URL inside `text` with `***@`."""
    return _CREDENTIAL_URL_RE.sub(r"\1***@", text)


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


def shallow_clone(clone_url: str, ref: str, dest: str, *,
                   timeout: int = 120) -> subprocess.CompletedProcess[str]:
    """Shallow-clone a repo, falling back to full clone + detached checkout for SHA refs.

    Returns the CompletedProcess of the successful clone (returncode == 0) or the
    last failed attempt.
    """
    def _run(cmd: list[str], timeout_msg: str) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(timeout_msg) from exc

    clone_timeout_msg = (
        f"git clone timed out after {timeout}s: {shlex.join(['git', 'clone', '--', clone_url])}"
    )

    result = _run(
        ["git", "clone", "--depth", "1", "--branch", ref, "--", clone_url, dest],
        clone_timeout_msg,
    )
    if result.returncode == 0:
        return result

    # --branch fails for SHA refs; fall back to a full clone + checkout --detach.
    # The fallback must NOT be shallow: a --depth 1 clone only contains the
    # default-branch tip, so `git checkout --detach <sha>` fails for any commit
    # that isn't the tip (fatal: unable to read tree). A full clone contains
    # every reachable commit, so an arbitrary historical SHA can be checked out.
    result = _run(["git", "clone", "--", clone_url, dest], clone_timeout_msg)
    if result.returncode != 0:
        return result

    checkout = _run(
        ["git", "-C", dest, "checkout", "--detach", ref],
        f"git checkout timed out after {timeout}s for ref {ref}",
    )
    if checkout.returncode != 0:
        # Return a failed result so the caller sees the error
        return checkout
    return result


def mapping_if_dict(value) -> dict | None:
    """Return value when it is a mapping; otherwise None."""

    return value if isinstance(value, dict) else None


def skill_contract_mapping(skill: dict) -> dict | None:
    """Return skill['contract'] only when it is a mapping (avoids .get chaining on scalars)."""

    return mapping_if_dict(skill.get("contract"))


def contract_metrics_as_dicts(metrics) -> list[dict]:
    """Metrics list entries that are mappings with an id (for rendering and tables)."""

    if metrics is None or not isinstance(metrics, list):
        return []
    return [m for m in metrics if isinstance(m, dict) and "id" in m]


def sequence_as_list(value) -> list:
    """Return a shallow copy when value is a list; otherwise an empty list."""

    return list(value) if isinstance(value, list) else []


def _plugin_field_value_for_touch_compare(plugin: dict, field: str):
    """Return a comparable value for plugin-level fields that can invalidate every skill."""

    if field == "strict":
        # Default when omitted is true (schema default). Explicit null aligns with default.
        if "strict" not in plugin:
            return True
        value = plugin["strict"]
        return value is None or bool(value)
    return plugin.get(field)


@dataclass(frozen=True, order=True)
class SkillKey:
    plugin_name: str
    skill_name: str


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as handle:
        return yaml.safe_load(handle) or {}


def normalize_git_ref(ref: str | None) -> str:
    """Normalize plugin ``source.ref`` for clone/checkout commands (defaults to ``main``)."""

    if ref is None:
        return "main"
    if not isinstance(ref, str):
        raise ValueError("source.ref must be a string when provided")

    normalized = ref.strip()
    if not normalized:
        return "main"
    if normalized.startswith("-"):
        raise ValueError("source.ref must not start with '-'")
    if any(
        character.isspace() or ord(character) < 32 or ord(character) == 127
        for character in normalized
    ):
        raise ValueError("source.ref must not contain whitespace or control characters")
    return normalized


def _validate_git_ref_token(ref: str) -> str:
    if not isinstance(ref, str):
        raise ValueError("git ref must be a string")

    normalized = ref.strip()
    if not normalized:
        raise ValueError("git ref must not be empty")
    if normalized.startswith("-"):
        raise ValueError("git ref must not start with '-'")
    if "\0" in normalized:
        raise ValueError("git ref must not contain null bytes")
    if any(character.isspace() or ord(character) < 32 or ord(character) == 127
           for character in normalized):
        raise ValueError("git ref must not contain whitespace or control characters")
    return normalized


def _validate_registry_path_token(path: str) -> str:
    if not isinstance(path, str):
        raise ValueError("registry path must be a string")

    normalized = path.strip()
    if not normalized:
        raise ValueError("registry path must not be empty")
    if normalized.startswith("-"):
        raise ValueError("registry path must not start with '-'")
    if "\0" in normalized or ":" in normalized:
        raise ValueError("registry path contains unsupported characters")

    path_obj = Path(normalized)
    if path_obj.is_absolute() or ".." in path_obj.parts:
        raise ValueError("registry path must stay within the repository")
    return normalized


def _run_git_read(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=GIT_READ_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"git command timed out after {GIT_READ_TIMEOUT_SECONDS}s: {' '.join(command)}"
        ) from exc


def load_registry_from_ref(ref: str, path: str = "registry.yaml") -> dict:
    safe_ref = _validate_git_ref_token(ref)
    safe_path = _validate_registry_path_token(path)
    _run_git_read(["git", "rev-parse", "--verify", "--quiet", f"{safe_ref}^{{object}}"])
    result = _run_git_read(["git", "show", f"{safe_ref}:{safe_path}"])
    return yaml.safe_load(result.stdout) or {}


def load_staged_registry(path: str = "registry.yaml") -> dict:
    safe_path = _validate_registry_path_token(path)
    result = _run_git_read(["git", "show", f":{safe_path}"])
    return yaml.safe_load(result.stdout) or {}


def iter_plugins(registry: dict):
    for plugin in registry.get("plugins", []):
        if isinstance(plugin, dict):
            yield plugin


def iter_skills(plugin: dict):
    for skill in plugin.get("skills", []):
        if isinstance(skill, dict):
            yield skill


def detect_touched_skills(before: dict, after: dict) -> list[SkillKey]:
    before_plugins = {plugin["name"]: plugin for plugin in iter_plugins(before) if "name" in plugin}
    after_plugins = {plugin["name"]: plugin for plugin in iter_plugins(after) if "name" in plugin}
    touched: set[SkillKey] = set()

    for plugin_name, after_plugin in after_plugins.items():
        before_plugin = before_plugins.get(plugin_name)
        after_skills = {skill["name"]: skill for skill in iter_skills(after_plugin) if "name" in skill}
        before_skills = {skill["name"]: skill for skill in iter_skills(before_plugin or {}) if "name" in skill}

        if before_plugin is None:
            touched.update(SkillKey(plugin_name, skill_name) for skill_name in after_skills)
            continue

        if any(
            _plugin_field_value_for_touch_compare(before_plugin, field)
            != _plugin_field_value_for_touch_compare(after_plugin, field)
            for field in PLUGIN_FIELDS_THAT_TOUCH_ALL_SKILLS
        ):
            touched.update(SkillKey(plugin_name, skill_name) for skill_name in after_skills)
            continue

        for skill_name, after_skill in after_skills.items():
            if before_skills.get(skill_name) != after_skill:
                touched.add(SkillKey(plugin_name, skill_name))

    return sorted(touched)
