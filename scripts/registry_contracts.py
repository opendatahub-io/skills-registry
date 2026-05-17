from __future__ import annotations

import subprocess
from dataclasses import dataclass

import yaml

CONTRACT_VERSION = "canonical-skill-v1"
SKILL_LINTER_VERSION = "0.1.4"
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


def load_registry_from_ref(ref: str, path: str = "registry.yaml") -> dict:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return yaml.safe_load(result.stdout) or {}


def load_staged_registry(path: str = "registry.yaml") -> dict:
    result = subprocess.run(
        ["git", "show", f":{path}"],
        capture_output=True,
        text=True,
        check=True,
    )
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
