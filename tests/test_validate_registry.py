import argparse
import importlib.util
import unittest
from pathlib import Path
from unittest import mock

from scripts.registry_contracts import SkillKey


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_validate_registry_module():
    module_path = REPO_ROOT / "scripts" / "validate_registry.py"
    spec = importlib.util.spec_from_file_location("validate_registry", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_VALIDATE_REGISTRY_MODULE = None


def get_validate_registry_module():
    global _VALIDATE_REGISTRY_MODULE
    if _VALIDATE_REGISTRY_MODULE is None:
        _VALIDATE_REGISTRY_MODULE = load_validate_registry_module()
    return _VALIDATE_REGISTRY_MODULE


def build_registry():
    return {
        "name": "example-registry",
        "owner": {"name": "example-org"},
        "plugins": [
            {
                "name": "example-plugin",
                "description": "Example plugin",
                "version": "1.0.0",
                "source": {"type": "github", "repo": "example-org/example-plugin"},
                "skills": [
                    {
                        "name": "example-skill",
                        "description": "Example skill",
                    }
                ],
            }
        ],
    }


def add_minimal_contract(skill):
    skill["contract"] = {
        "version": "canonical-skill-v1",
        "functions": ["review"],
        "metrics": [{"id": "task_success", "measure": "deterministic"}],
        "problem_statement": (
            "Review the supplied artifact and produce the correct recommendation."
        ),
        "success_conditions": [
            "Produces the expected recommendation for the supplied artifact."
        ],
        "invariants": {
            "must_preserve": [
                "Do not invent or omit evidence.",
            ],
            "fixed_context": {
                "tools": ["Read"],
                "knowledge_inputs": [
                    {"kind": "repository_content", "privacy": "public"}
                ],
            },
        },
        "source_assertions": {
            "skill_path": "skills/example-skill/SKILL.md"
        },
    }


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mod = get_validate_registry_module()
        if mod.jsonschema is None:
            raise unittest.SkipTest("jsonschema is required for schema validation tests")
        cls.validate_registry = mod
        cls.schema = mod.load_schema(str(REPO_ROOT / "schema/registry.schema.json"))

    def test_schema_accepts_minimal_contract_block(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_accepts_plugin_contract_summary(self):
        registry = build_registry()
        registry["plugins"][0]["contract_summary"] = {
            "focus_functions": ["review"],
            "focus_metrics": ["task_success"],
            "notes": "Example summary",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_rejects_unknown_function_value(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["functions"] = ["rank"]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("rank" in error for error in errors), errors)

    def test_schema_requires_rubric_for_judge_measure(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["metrics"] = [
            {"id": "output_quality", "measure": "judge"}
        ]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("rubric_ref" in error for error in errors), errors)

    def test_schema_requires_verifier_ref_for_verifier_backed_measure(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["metrics"] = [
            {"id": "task_success", "measure": "verifier_backed"}
        ]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("verifier_ref" in error for error in errors), errors)

    def test_schema_rejects_legacy_evaluation_field(self):
        registry = build_registry()
        registry["plugins"][0]["skills"][0]["evaluation"] = {
            "contract": "canonical-skill-v1",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("evaluation" in error for error in errors), errors)

    def test_schema_rejects_empty_fixed_context(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["invariants"]["fixed_context"] = {}

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertNotEqual([], errors, errors)
        path_prefixes = [error.split(":", 1)[0].strip() for error in errors]
        self.assertTrue(
            any(path.endswith("fixed_context") for path in path_prefixes),
            errors,
        )

    def test_schema_rejects_output_quality_with_deterministic_measure(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["metrics"] = [
            {"id": "output_quality", "measure": "deterministic"}
        ]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertNotEqual([], errors, errors)
        self.assertTrue(
            any("judge" in error or "deterministic" in error for error in errors),
            errors,
        )

    def test_schema_rejects_latency_with_judge_measure(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["metrics"] = [
            {"id": "latency", "measure": "judge"}
        ]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertNotEqual([], errors, errors)
        self.assertTrue(
            any("deterministic" in error or "judge" in error for error in errors),
            errors,
        )

    def test_schema_accepts_step_efficiency_with_deterministic_measure(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["metrics"] = [
            {"id": "step_efficiency", "measure": "deterministic"}
        ]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_requires_measure_for_metric_assignment(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["metrics"] = [{"id": "latency"}]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("measure" in error for error in errors), errors)


class ContractValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_registry = get_validate_registry_module()

    def test_touched_skill_without_contract_fails(self):
        registry = build_registry()
        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )
        self.assertTrue(any("requires contract" in error for error in errors), errors)

    def test_untouched_skill_without_contract_passes(self):
        registry = build_registry()
        errors = self.validate_registry.check_skill_contracts(registry, required_skills=set())
        self.assertEqual([], errors)

    def test_duplicate_metric_ids_fail(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["metrics"] = [{"id": "task_success"}, {"id": "task_success"}]

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(any("duplicate metric" in error.lower() for error in errors), errors)

    def test_judge_measure_requires_rubric_ref(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["metrics"] = [{"id": "task_success", "measure": "judge"}]

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(any("rubric_ref" in error for error in errors), errors)

    def test_output_quality_requires_rubric_ref_when_measure_omitted(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["metrics"] = [{"id": "output_quality"}]

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(any("output_quality metric requires" in e for e in errors), errors)
        self.assertTrue(any("rubric_ref" in e for e in errors), errors)

    def test_untouched_skill_with_invalid_contract_passes(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["metrics"] = [{"id": "task_success"}, {"id": "task_success"}]

        errors = self.validate_registry.check_skill_contracts(registry, required_skills=set())

        self.assertEqual([], errors)

    def test_touched_skill_whitespace_skill_path_fails(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["source_assertions"]["skill_path"] = "  \t  "

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(any("skill_path" in e for e in errors), errors)

    def test_touched_skill_skill_path_must_reference_skill_md(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["source_assertions"]["skill_path"] = (
            "skills/example-skill/not-skill.md"
        )

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(
            any("skill_path" in e.lower() or "SKILL.md" in e for e in errors),
            errors,
        )

    def test_touched_skill_verifier_backed_without_verifier_ref_fails(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["metrics"] = [{"id": "task_success", "measure": "verifier_backed"}]

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(any("verifier_ref" in e for e in errors), errors)

    def test_touched_skill_duplicate_functions_fail(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["functions"] = ["review", "review"]

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(any("duplicate function" in e.lower() for e in errors), errors)

    def test_touched_skill_placeholder_problem_statement_fails(self):
        registry = build_registry()
        skill = registry["plugins"][0]["skills"][0]
        add_minimal_contract(skill)
        skill["contract"]["problem_statement"] = "TODO: replace with a real problem statement."

        errors = self.validate_registry.check_skill_contracts(
            registry,
            required_skills={SkillKey("example-plugin", "example-skill")},
        )

        self.assertTrue(any("placeholder" in e.lower() for e in errors), errors)

    def test_select_required_skills_missing_diff_base_returns_error(self):
        args = argparse.Namespace(
            registry="registry.yaml",
            staged=False,
            diff_base="__skills_registry_nonexistent_git_ref__",
        )
        required, errs = self.validate_registry.select_required_skills(args, build_registry())

        self.assertEqual(set(), required)
        self.assertTrue(len(errs) >= 1, errs)
        self.assertTrue(
            any("git ref" in e.lower() or "could not load" in e.lower() for e in errs),
            errs,
        )


class RemotePluginValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_registry = get_validate_registry_module()

    @mock.patch("subprocess.run")
    def test_validate_remote_plugin_rejects_invalid_ref_before_git(self, run_mock):
        plugin = {
            "name": "example-plugin",
            "source": {
                "type": "github",
                "repo": "example-org/example-plugin",
                "ref": "-oops",
            },
        }

        errors = self.validate_registry.validate_remote_plugin(plugin)

        self.assertTrue(any("invalid source.ref" in error for error in errors), errors)
        run_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
