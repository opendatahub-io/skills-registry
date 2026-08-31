import argparse
import importlib.util
import subprocess
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

    def test_schema_accepts_skill_count_and_includes(self):
        registry = build_registry()
        registry["plugins"][0]["skill_count"] = 7
        registry["plugins"].append({
            "name": "bundle-plugin",
            "description": "A bundle",
            "version": "1.0.0",
            "source": {"type": "github", "repo": "example-org/bundle"},
            "includes": ["example-plugin"],
        })

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_accepts_mcp_servers(self):
        registry = build_registry()
        registry["plugins"][0]["mcp_servers"] = [
            {"name": "patternfly", "description": "Component docs via MCP"}
        ]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_rejects_mcp_server_without_description(self):
        registry = build_registry()
        registry["plugins"][0]["mcp_servers"] = [{"name": "patternfly"}]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertNotEqual([], errors)

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

    def test_schema_rejects_traversal_skill_path(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["source_assertions"]["skill_path"] = (
            "../outside/SKILL.md"
        )

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertNotEqual([], errors, errors)
        self.assertTrue(any("skill_path" in error for error in errors), errors)

    def test_schema_rejects_absolute_supporting_path(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["source_assertions"]["supporting_paths"] = [
            "/tmp/guide.md"
        ]

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertNotEqual([], errors, errors)
        self.assertTrue(any("supporting_paths" in error for error in errors), errors)

    def test_schema_accepts_git_source_with_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.corp.example.com/team/my-plugin.git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_rejects_git_source_without_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("url" in error for error in errors), errors)

    def test_schema_rejects_github_source_without_repo(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "github",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("repo" in error for error in errors), errors)

    def test_schema_rejects_git_source_with_repo(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
            "repo": "team/plugin",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("repo" in error for error in errors), errors)

    def test_schema_rejects_github_source_with_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "github",
            "repo": "example-org/example-plugin",
            "url": "https://github.com/example-org/example-plugin.git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("url" in error for error in errors), errors)

    def test_schema_rejects_non_https_git_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "git@gitlab.example.com:team/plugin.git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("url" in error for error in errors), errors)

    def test_schema_rejects_git_url_with_embedded_credentials(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://user:token@gitlab.example.com/team/plugin.git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("url" in error for error in errors), errors)

    def test_schema_rejects_git_subdir_url_with_embedded_credentials(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://oauth2:SECRET@github.com/acme/monorepo.git",
            "path": "tools/plugin",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("url" in error for error in errors), errors)

    def test_schema_accepts_https_git_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
            "ref": "main",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_requires_url_and_path_for_git_subdir(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {"type": "git-subdir", "ref": "main"}

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(errors)

    def test_schema_accepts_git_subdir_with_url_and_path(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://github.com/acme/monorepo.git",
            "path": "tools/plugin",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)

    def test_schema_rejects_non_https_git_subdir_url(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "git@github.com:acme/monorepo.git",
            "path": "tools/plugin",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("url" in error for error in errors), errors)

    def test_schema_rejects_git_subdir_source_with_repo(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://github.com/acme/monorepo.git",
            "path": "tools/plugin",
            "repo": "acme/monorepo",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(any("repo" in error for error in errors), errors)

    def test_schema_rejects_blank_git_subdir_path(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://github.com/acme/monorepo.git",
            "path": "   ",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(errors, "a blank git-subdir path must be rejected")

    def test_schema_rejects_git_subdir_path_with_traversal(self):
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://github.com/acme/monorepo.git",
            "path": "../escape",
        }

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertTrue(errors, "a git-subdir path with '..' must be rejected")

    def test_schema_accepts_dot_prefixed_skill_path(self):
        registry = build_registry()
        add_minimal_contract(registry["plugins"][0]["skills"][0])
        registry["plugins"][0]["skills"][0]["contract"]["source_assertions"]["skill_path"] = (
            ".claude/skills/example-skill/SKILL.md"
        )

        errors = self.validate_registry.validate_schema(registry, self.schema)

        self.assertEqual([], errors)


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

    def test_select_required_skills_invalid_diff_base_returns_error(self):
        args = argparse.Namespace(
            registry="registry.yaml",
            staged=False,
            diff_base="-oops",
        )
        required, errs = self.validate_registry.select_required_skills(args, build_registry())

        self.assertEqual(set(), required)
        self.assertTrue(errs, errs)
        self.assertTrue(
            any("git ref" in e.lower() or "could not load" in e.lower() for e in errs),
            errs,
        )


class RemotePluginValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_registry = get_validate_registry_module()

    @mock.patch("subprocess.run")
    def test_check_sources_uses_ls_remote_for_git_type(self, run_mock):
        run_mock.return_value = subprocess.CompletedProcess(
            ["git", "ls-remote"], 0, stdout="", stderr=""
        )
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
        }

        errors = self.validate_registry.check_sources(registry)

        self.assertEqual([], errors)
        run_mock.assert_called_once()
        cmd = run_mock.call_args[0][0]
        self.assertEqual(cmd[0], "git")
        self.assertIn("ls-remote", cmd)
        self.assertIn("--", cmd)

    @mock.patch("subprocess.run")
    def test_validate_remote_plugin_accepts_git_type(self, run_mock):
        import tempfile
        import os

        run_mock.return_value = subprocess.CompletedProcess(
            ["git", "clone"], 0, stdout="", stderr=""
        )
        plugin = {
            "name": "git-plugin",
            "source": {
                "type": "git",
                "url": "https://gitlab.example.com/team/plugin.git",
                "ref": "main",
            },
        }

        real_tmpdir = tempfile.mkdtemp()
        try:
            # Set up the directory structure that post-clone validation expects
            plugin_dir = os.path.join(real_tmpdir, ".claude-plugin")
            os.makedirs(plugin_dir)
            with open(os.path.join(plugin_dir, "plugin.json"), "w") as f:
                f.write('{"name": "git-plugin", "version": "1.0.0"}')
            skill_dir = os.path.join(real_tmpdir, "skills", "example-skill")
            os.makedirs(skill_dir)
            with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
                f.write("# Example Skill")

            ctx = mock.MagicMock()
            ctx.__enter__ = mock.Mock(return_value=real_tmpdir)
            ctx.__exit__ = mock.Mock(return_value=False)
            with mock.patch("tempfile.TemporaryDirectory", return_value=ctx):
                errors = self.validate_registry.validate_remote_plugin(plugin)

            self.assertTrue(run_mock.called)
            cmd = run_mock.call_args[0][0]
            self.assertIn("https://gitlab.example.com/team/plugin.git", cmd)
            self.assertEqual([], errors)
        finally:
            import shutil
            shutil.rmtree(real_tmpdir)

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


class SkillNameDriftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_registry = get_validate_registry_module()

    @staticmethod
    def write_skill(root: Path, relative_dir: str, name: str, user_invocable=None):
        skill_dir = root / relative_dir / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        lines = ["---", f"name: {name}", "description: A skill."]
        if user_invocable is not None:
            lines.append(f"user-invocable: {str(user_invocable).lower()}")
        lines += ["---", "", f"# {name}", ""]
        (skill_dir / "SKILL.md").write_text("\n".join(lines), encoding="utf-8")

    def check(self, plugin, build):
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build(root)
            return self.validate_registry.check_skill_names_against_source(plugin, root)

    def test_registry_name_without_upstream_skill_is_an_error(self):
        plugin = {"name": "p", "skills": [{"name": "knowledge.repo"}]}
        errors, _ = self.check(
            plugin, lambda root: self.write_skill(root, "skills", "knowledge-repo")
        )

        self.assertEqual(1, len(errors), errors)
        self.assertIn("knowledge.repo", errors[0])
        self.assertIn("knowledge-repo", errors[0])

    def test_matching_names_produce_nothing(self):
        plugin = {"name": "p", "skills": [{"name": "alpha"}, {"name": "beta"}]}
        errors, warnings = self.check(
            plugin,
            lambda root: [
                self.write_skill(root, "skills", "alpha"),
                self.write_skill(root, "skills", "beta"),
            ],
        )

        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_user_invocable_disagreement_warns_but_does_not_fail(self):
        plugin = {"name": "p", "skills": [{"name": "alpha", "user-invocable": False}]}
        # Upstream omits the key, so it resolves to the Claude Code default of true.
        errors, warnings = self.check(
            plugin, lambda root: self.write_skill(root, "skills", "alpha")
        )

        self.assertEqual([], errors)
        self.assertEqual(1, len(warnings), warnings)
        self.assertIn("user-invocable", warnings[0])

    def test_unlisted_upstream_skills_warn_only_for_non_strict_plugins(self):
        def build(root):
            self.write_skill(root, "skills", "alpha")
            self.write_skill(root, "skills", "extra")

        strict_plugin = {"name": "p", "skills": [{"name": "alpha"}]}
        errors, warnings = self.check(strict_plugin, build)
        self.assertEqual([], errors)
        self.assertEqual([], warnings, "strict: true registry lists are curated subsets")

        loose_plugin = {"name": "p", "strict": False, "skills": [{"name": "alpha"}]}
        errors, warnings = self.check(loose_plugin, build)
        self.assertEqual([], errors)
        self.assertEqual(1, len(warnings), warnings)
        self.assertIn("extra", warnings[0])

    def test_only_the_first_populated_skills_dir_is_used(self):
        # A repo can publish skills/ while keeping its own tooling in .claude/skills/.
        def build(root):
            self.write_skill(root, "skills", "alpha")
            self.write_skill(root, ".claude/skills", "repo-local-tooling")

        plugin = {"name": "p", "strict": False, "skills": [{"name": "alpha"}]}
        errors, warnings = self.check(plugin, build)

        self.assertEqual([], errors)
        self.assertEqual([], warnings, "tooling in .claude/skills must not be reported")

    def test_directory_name_is_the_fallback_when_frontmatter_omits_name(self):
        def build(root):
            skill_dir = root / "skills" / "alpha"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\ndescription: No name key.\n---\n\n# alpha\n", encoding="utf-8"
            )

        plugin = {"name": "p", "skills": [{"name": "alpha"}]}
        errors, warnings = self.check(plugin, build)

        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_repo_without_any_skill_md_is_left_to_remote_validation(self):
        plugin = {"name": "p", "skills": [{"name": "alpha"}]}
        errors, warnings = self.check(plugin, lambda root: None)

        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_diff_touched_plugins_lists_changed_entries(self):
        base = {"plugins": [{"name": "a", "version": "1"}, {"name": "b", "version": "1"}]}
        current = {"plugins": [{"name": "a", "version": "2"}, {"name": "b", "version": "1"}]}

        with mock.patch.object(self.validate_registry, "load_registry_from_ref",
                               return_value=base):
            self.assertEqual(["a"],
                             self.validate_registry.diff_touched_plugins(current, "origin/main"))

    def test_diff_touched_plugins_returns_none_when_base_is_unreadable(self):
        with mock.patch.object(self.validate_registry, "load_registry_from_ref",
                               side_effect=ValueError("no such ref")):
            self.assertIsNone(
                self.validate_registry.diff_touched_plugins({"plugins": []}, "origin/nope")
            )


class BundleCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_registry = get_validate_registry_module()

    def _registry(self, bundle_overrides=None):
        bundle = {
            "name": "bundle",
            "description": "d",
            "version": "1.0.0",
            "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "a"},
            "includes": ["leaf"],
        }
        if bundle_overrides:
            bundle.update(bundle_overrides)
        return {
            "name": "r",
            "owner": {"name": "o"},
            "plugins": [
                bundle,
                {
                    "name": "leaf",
                    "description": "d",
                    "version": "1.0.0",
                    "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "b"},
                    "skill_count": 3,
                },
            ],
        }

    def test_valid_bundle_passes(self):
        self.assertEqual([], self.validate_registry.check_bundles(self._registry()))

    def test_unknown_member_errors(self):
        errors = self.validate_registry.check_bundles(
            self._registry({"includes": ["leaf", "ghost"]}))
        self.assertEqual(1, len(errors))
        self.assertIn("ghost", errors[0])

    def test_bundle_with_own_skill_count_errors(self):
        errors = self.validate_registry.check_bundles(
            self._registry({"skill_count": 5}))
        self.assertTrue(any("skill_count" in e for e in errors))

    def test_bundle_with_own_skills_errors(self):
        errors = self.validate_registry.check_bundles(
            self._registry({"skills": [{"name": "s", "description": "d"}]}))
        self.assertTrue(any("skills" in e for e in errors))

    def test_bundle_listing_itself_errors(self):
        errors = self.validate_registry.check_bundles(
            self._registry({"includes": ["bundle"]}))
        self.assertTrue(any("itself" in e for e in errors))

    def test_member_cycle_errors(self):
        registry = {
            "name": "r", "owner": {"name": "o"},
            "plugins": [
                {"name": "a", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "a"},
                 "includes": ["b"]},
                {"name": "b", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "b"},
                 "includes": ["a"]},
            ],
        }
        errors = self.validate_registry.check_bundles(registry)
        self.assertTrue(any("cycle" in e for e in errors))

    def test_leaf_with_skill_count_and_skills_errors(self):
        registry = {
            "name": "r", "owner": {"name": "o"},
            "plugins": [
                {"name": "leaf", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "b"},
                 "skill_count": 5,
                 "skills": [{"name": "s", "description": "d"}]},
            ],
        }
        errors = self.validate_registry.check_bundles(registry)
        self.assertTrue(any("skill_count" in e and "skills" in e for e in errors))

    def test_leaf_with_skill_count_and_empty_skills_errors(self):
        # Presence-based: an empty skills array alongside skill_count is still
        # a contract violation.
        registry = {
            "name": "r", "owner": {"name": "o"},
            "plugins": [
                {"name": "leaf", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "b"},
                 "skill_count": 5, "skills": []},
            ],
        }
        errors = self.validate_registry.check_bundles(registry)
        self.assertTrue(any("skill_count" in e and "skills" in e for e in errors))

    def test_empty_includes_errors(self):
        errors = self.validate_registry.check_bundles(
            self._registry({"includes": []}))
        self.assertTrue(any("empty includes" in e for e in errors))

    def test_nested_bundle_errors(self):
        # A bundle member may not itself be a bundle (nesting unsupported).
        registry = {
            "name": "r", "owner": {"name": "o"},
            "plugins": [
                {"name": "a", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "a"},
                 "includes": ["b"]},
                {"name": "b", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "b"},
                 "includes": ["c"]},
                {"name": "c", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "c"},
                 "skill_count": 1},
            ],
        }
        errors = self.validate_registry.check_bundles(registry)
        self.assertTrue(any("nested bundles are not supported" in e for e in errors))


class ContractSourceExemptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_registry = get_validate_registry_module()

    def _registry(self):
        return {
            "name": "r", "owner": {"name": "o"},
            "plugins": [
                {"name": "gh", "description": "d", "version": "1.0.0",
                 "source": {"type": "github", "repo": "o/r"},
                 "skills": [{"name": "s1", "description": "d"}]},
                {"name": "sub", "description": "d", "version": "1.0.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p"},
                 "skills": [{"name": "s2", "description": "d"}]},
            ],
        }

    def test_git_subdir_skill_exempt_from_contract(self):
        reg = self._registry()
        required = {SkillKey("sub", "s2")}
        errors = self.validate_registry.check_skill_contracts(reg, required)
        self.assertEqual([], errors)

    def test_github_skill_still_requires_contract(self):
        # Hole-closed: a cloneable-source plugin's contract-less skill is flagged
        # even when it is a bundle member.
        reg = self._registry()
        reg["plugins"].append({
            "name": "bundle", "description": "d", "version": "1.0.0",
            "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "b"},
            "includes": ["gh"],
        })
        required = {SkillKey("gh", "s1")}
        errors = self.validate_registry.check_skill_contracts(reg, required)
        self.assertTrue(any("gh" in e and "s1" in e for e in errors))


class SourceSubdirTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vr = get_validate_registry_module()

    def test_whole_repo_source_returns_empty(self):
        self.assertEqual("", self.vr.source_subdir({"type": "github", "repo": "o/r"}))
        self.assertEqual("", self.vr.source_subdir({"type": "git", "url": "https://x/y.git"}))

    def test_non_string_path_returns_empty_not_crash(self):
        # Unreachable after schema validation, but the helper must never raise.
        self.assertEqual("", self.vr.source_subdir({"type": "git-subdir", "url": "u", "path": 1}))
        self.assertEqual("", self.vr.source_subdir({"type": "git-subdir", "url": "u"}))

    def test_normalizes_dot_slash_and_leading_slash(self):
        self.assertEqual(
            "a/b", self.vr.source_subdir({"type": "git-subdir", "url": "u", "path": "./a/b"}))
        self.assertEqual(
            "a/b", self.vr.source_subdir({"type": "git-subdir", "url": "u", "path": "/a/b"}))


class PluginRootInCloneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vr = get_validate_registry_module()

    def test_whole_repo_source_returns_repo_root(self):
        root = Path("/tmp/clone-xyz")
        self.assertEqual(
            root,
            self.vr._plugin_root_in_clone(root, {"type": "github", "repo": "o/r"}),
        )

    def test_git_subdir_roots_at_subdirectory(self):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "plugins", "pf-react"))
            got = self.vr._plugin_root_in_clone(
                Path(d),
                {"type": "git-subdir", "url": "https://x/y.git", "path": "plugins/pf-react"},
            )
            self.assertEqual(Path(d, "plugins", "pf-react").resolve(), got.resolve())

    def test_traversal_subdir_is_rejected(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(
                self.vr._plugin_root_in_clone(
                    Path(d),
                    {"type": "git-subdir", "url": "https://x/y.git", "path": "../escape"},
                )
            )


class RunOnClonesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vr = get_validate_registry_module()

    def test_dedupes_clone_per_repo_ref_and_roots_at_subdir(self):
        import os

        members = [
            {"name": "pf-a", "source": {"type": "git-subdir",
                                        "url": "https://x/y.git", "path": "plugins/a"}},
            {"name": "pf-b", "source": {"type": "git-subdir",
                                        "url": "https://x/y.git", "path": "plugins/b"}},
        ]
        clone_calls = []

        def fake_clone(url, ref, dest, **kwargs):
            clone_calls.append((url, ref))
            os.makedirs(os.path.join(dest, "plugins", "a"))
            os.makedirs(os.path.join(dest, "plugins", "b"))
            return subprocess.CompletedProcess(["git", "clone"], 0, "", "")

        seen = {}

        def per_plugin(plugin, root):
            seen[plugin["name"]] = os.path.basename(str(root))
            return [], [f"w:{plugin['name']}"]

        with mock.patch.object(self.vr, "shallow_clone", side_effect=fake_clone):
            errors, warnings = self.vr.run_on_clones(members, per_plugin)

        self.assertEqual(1, len(clone_calls), "one clone per (url, ref) — members share it")
        self.assertEqual({"pf-a": "a", "pf-b": "b"}, seen)
        self.assertEqual([], errors)
        self.assertEqual({"w:pf-a", "w:pf-b"}, set(warnings))

    def test_clone_failure_warns_and_skips_per_plugin(self):
        members = [{"name": "p", "source": {"type": "github", "repo": "o/r"}}]

        def fake_clone(url, ref, dest, **kwargs):
            return subprocess.CompletedProcess(["git", "clone"], 128, "", "boom")

        called = []

        with mock.patch.object(self.vr, "shallow_clone", side_effect=fake_clone):
            errors, warnings = self.vr.run_on_clones(
                members, lambda p, root: (called.append(p["name"]) or ([], [])))

        self.assertEqual([], called, "per_plugin must not run on clone failure")
        self.assertEqual([], errors)
        self.assertEqual(1, len(warnings))
        self.assertIn("could not clone", warnings[0])

    def test_missing_subdir_warns_and_skips_per_plugin(self):
        members = [{"name": "p", "source": {"type": "git-subdir",
                                            "url": "https://x/y.git", "path": "nope"}}]

        def fake_clone(url, ref, dest, **kwargs):
            return subprocess.CompletedProcess(["git", "clone"], 0, "", "")

        def per_plugin(plugin, root):
            raise AssertionError("per_plugin must not run when the subdir is missing")

        with mock.patch.object(self.vr, "shallow_clone", side_effect=fake_clone):
            errors, warnings = self.vr.run_on_clones(members, per_plugin)

        self.assertEqual([], errors)
        self.assertEqual(1, len(warnings))
        self.assertIn("nope", warnings[0])

    def test_non_cloneable_sources_are_skipped(self):
        members = [
            {"name": "npm-plugin", "source": {"type": "npm"}},
            {"name": "local-plugin", "source": {"type": "local"}},
        ]

        def fake_clone(url, ref, dest, **kwargs):
            raise AssertionError("no clone should happen for npm/local sources")

        with mock.patch.object(self.vr, "shallow_clone", side_effect=fake_clone):
            errors, warnings = self.vr.run_on_clones(members, lambda p, root: ([], []))

        self.assertEqual([], errors)
        self.assertEqual([], warnings)


class CodexManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vr = get_validate_registry_module()

    @staticmethod
    def _root(tmp, *, codex=False, claude=False):
        import os

        if codex:
            os.makedirs(os.path.join(tmp, ".codex-plugin"))
            (Path(tmp) / ".codex-plugin" / "plugin.json").write_text("{}")
        if claude:
            os.makedirs(os.path.join(tmp, ".claude-plugin"))
            (Path(tmp) / ".claude-plugin" / "plugin.json").write_text("{}")
        return Path(tmp)

    def _check(self, plugin, **root_kwargs):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            return self.vr.check_codex_manifest(plugin, self._root(d, **root_kwargs))

    def test_warns_when_manifest_missing_and_plugin_has_skills(self):
        errors, warnings = self._check({"name": "p", "skills": [{"name": "s"}]})
        self.assertEqual([], errors)
        self.assertEqual(1, len(warnings))
        self.assertIn(".codex-plugin/plugin.json", warnings[0])

    def test_warns_for_skill_count_only_plugin(self):
        errors, warnings = self._check({"name": "p", "skill_count": 4})
        self.assertEqual(1, len(warnings), warnings)

    def test_silent_when_codex_manifest_present(self):
        errors, warnings = self._check({"name": "p", "skills": [{"name": "s"}]}, codex=True)
        self.assertEqual(([], []), (errors, warnings))

    def test_silent_for_bundle_meta_plugin(self):
        errors, warnings = self._check({"name": "b", "includes": ["x"]})
        self.assertEqual(([], []), (errors, warnings))

    def test_silent_when_plugin_declares_no_skills(self):
        errors, warnings = self._check({"name": "mcp-only"})
        self.assertEqual(([], []), (errors, warnings))

    def test_never_returns_errors(self):
        errors, _ = self._check({"name": "p", "skills": [{"name": "s"}]})
        self.assertEqual([], errors, "Codex readiness is warn-only, never a blocking error")

    def test_hint_mentions_claude_manifest_when_present(self):
        _, warnings = self._check({"name": "p", "skills": [{"name": "s"}]}, claude=True)
        self.assertEqual(1, len(warnings))
        self.assertIn(".claude-plugin/plugin.json", warnings[0])


class GitSubdirSourceCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validate_registry = get_validate_registry_module()

    @mock.patch("subprocess.run")
    def test_check_sources_ls_remotes_git_subdir_repo_url(self, run_mock):
        run_mock.return_value = subprocess.CompletedProcess(
            ["git", "ls-remote"], 0, stdout="", stderr=""
        )
        registry = build_registry()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://github.com/acme/monorepo.git",
            "path": "tools/plugin",
        }

        errors = self.validate_registry.check_sources(registry)

        self.assertEqual([], errors)
        run_mock.assert_called_once()
        cmd = run_mock.call_args[0][0]
        self.assertIn("ls-remote", cmd)
        self.assertIn("https://github.com/acme/monorepo.git", cmd)


if __name__ == "__main__":
    unittest.main()
