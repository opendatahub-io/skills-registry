"""Shared registry dicts for contract rendering tests."""

from __future__ import annotations

import copy


MINIMAL_CONTRACT = {
    "version": "canonical-skill-v1",
    "functions": ["review"],
    "metrics": [
        {"id": "task_success", "measure": "deterministic"},
        {
            "id": "output_quality",
            "measure": "judge",
            "rubric_ref": "example-org/example-plugin@main:docs/review-rubric.md",
        },
    ],
    "problem_statement": "Review the artifact.",
    "success_conditions": ["Produce the correct review."],
    "invariants": {
        "must_preserve": ["Do not invent evidence."],
        "fixed_context": {
            "tools": ["Read"],
            "knowledge_inputs": [{"kind": "repository_content", "privacy": "public"}],
        },
    },
    "source_assertions": {"skill_path": "skills/example-skill/SKILL.md"},
}


def build_registry_with_contract() -> dict:
    """Minimal registry shaped like the real marketplace (plugin + categorized skill)."""

    return {
        "name": "example-registry",
        "description": "Example Registry",
        "owner": {"name": "example-org"},
        "categories": {"evaluation": {"name": "Evaluation", "description": "Eval tools"}},
        "plugins": [
            {
                "name": "example-plugin",
                "description": "Example plugin",
                "version": "1.0.0",
                "category": "evaluation",
                "source": {"type": "github", "repo": "example-org/example-plugin"},
                "skills": [
                    {
                        "name": "example-skill",
                        "description": "Example skill",
                        "contract": copy.deepcopy(MINIMAL_CONTRACT),
                    }
                ],
            }
        ],
    }
