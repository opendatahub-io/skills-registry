import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.run_skill_linter import (
    _select_touched_skill_keys,
    build_skill_linter_command,
    interpret_skill_linter_success_stdout,
    normalize_git_ref,
    parse_skill_linter_output,
    run_captured_command,
    skill_is_skill_linter_candidate,
    skill_linter_dir_from_contract_skill_path,
    validate_source_assertions,
)


class SkillLinterWrapperTests(unittest.TestCase):
    def test_build_command_pins_version_and_config(self):
        command = build_skill_linter_command(
            Path("/tmp/cache/repo/skills/example-skill"),
            Path("/work/config/skill-linter-registry.json"),
        )

        self.assertEqual(
            [
                "npx",
                "--yes",
                "--package",
                "skill-linter@0.1.4",
                "skill-linter",
                "check",
                "/tmp/cache/repo/skills/example-skill",
                "--format",
                "json",
                "--config",
                "/work/config/skill-linter-registry.json",
            ],
            command,
        )

    def test_validate_source_assertions_rejects_missing_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            with self.assertRaises(FileNotFoundError):
                validate_source_assertions(repo_root, "skills/missing/SKILL.md", [])

    def test_validate_source_assertions_rejects_escaping_skill_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            repo_root = base / "repo"
            repo_root.mkdir()
            outside = base / "outside"
            outside.mkdir()
            (outside / "SKILL.md").write_text("outside skill", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                validate_source_assertions(repo_root, "../outside/SKILL.md", [])

    def test_validate_source_assertions_rejects_escaping_supporting_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            repo_root = base / "repo"
            repo_root.mkdir()
            skills = repo_root / "skills"
            skills.mkdir()
            (skills / "SKILL.md").write_text("inside", encoding="utf-8")
            outside = base / "outside"
            outside.mkdir()
            (outside / "extra.md").write_text("outside", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                validate_source_assertions(repo_root, "skills/SKILL.md", ["../outside/extra.md"])

    def test_validate_source_assertions_rejects_missing_supporting_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            skills = repo_root / "skills"
            skills.mkdir()
            (skills / "SKILL.md").write_text("inside", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                validate_source_assertions(repo_root, "skills/SKILL.md", ["skills/missing-extra.md"])

    def test_validate_source_assertions_rejects_symlinked_skill_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            real_skill_dir = repo_root / "real-skill"
            real_skill_dir.mkdir()
            (real_skill_dir / "SKILL.md").write_text("inside", encoding="utf-8")
            link_dir = repo_root / "skills"
            link_dir.mkdir()
            try:
                (link_dir / "SKILL.md").symlink_to(real_skill_dir / "SKILL.md")
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")
            with self.assertRaises(FileNotFoundError):
                validate_source_assertions(repo_root, "skills/SKILL.md", [])

    def test_validate_source_assertions_rejects_symlinked_supporting_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            skills = repo_root / "skills"
            skills.mkdir()
            (skills / "SKILL.md").write_text("inside", encoding="utf-8")
            support_dir = repo_root / "support"
            support_dir.mkdir()
            (support_dir / "guide.md").write_text("guide", encoding="utf-8")
            try:
                (skills / "guide.md").symlink_to(support_dir / "guide.md")
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")
            with self.assertRaises(FileNotFoundError):
                validate_source_assertions(repo_root, "skills/SKILL.md", ["skills/guide.md"])

    def test_parse_output_rejects_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_skill_linter_output("not-json")

    def test_parse_output_rejects_non_object_json(self):
        with self.assertRaises(ValueError):
            parse_skill_linter_output("[]")

    def test_skill_linter_dir_requires_skill_md_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "skills" / "foo").mkdir(parents=True)
            (root / "skills" / "foo" / "SKILL.md").write_text("x", encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                skill_linter_dir_from_contract_skill_path(root, "skills/foo")
            self.assertIn("SKILL.md", str(ctx.exception))

    def test_skill_linter_dir_returns_parent_of_skill_md(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            skill_dir = root / "skills" / "foo"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("x", encoding="utf-8")
            self.assertEqual(
                skill_dir.resolve(),
                skill_linter_dir_from_contract_skill_path(root, "skills/foo/SKILL.md"),
            )

    def test_skill_linter_dir_rejects_symlinked_skill_md(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            real_dir = root / "real"
            real_dir.mkdir(parents=True)
            (real_dir / "SKILL.md").write_text("x", encoding="utf-8")
            link_dir = root / "skills" / "foo"
            link_dir.mkdir(parents=True)
            try:
                (link_dir / "SKILL.md").symlink_to(real_dir / "SKILL.md")
            except OSError as exc:
                self.skipTest(f"symlinks unavailable: {exc}")
            with self.assertRaises(FileNotFoundError):
                skill_linter_dir_from_contract_skill_path(root, "skills/foo/SKILL.md")

    def test_interpret_stdout_accepts_empty(self):
        self.assertEqual(interpret_skill_linter_success_stdout(""), (True, None))
        self.assertEqual(interpret_skill_linter_success_stdout("\n\t  "), (True, None))

    def test_interpret_stdout_accepts_empty_object_json(self):
        ok, detail = interpret_skill_linter_success_stdout("{}")
        self.assertTrue(ok)
        self.assertIsNone(detail)

    def test_interpret_stdout_rejects_nonempty_non_json_on_success(self):
        ok, detail = interpret_skill_linter_success_stdout("{not json")
        self.assertFalse(ok)
        self.assertIsNotNone(detail)
        self.assertIn("JSON", detail)

    def test_interpret_stdout_rejects_reports_with_errors(self):
        payload = '{"errorCount": 1, "violations": []}'
        ok, detail = interpret_skill_linter_success_stdout(payload)
        self.assertFalse(ok)
        self.assertIsNotNone(detail)
        self.assertIn("errorCount", detail)

    def test_interpret_stdout_rejects_nonnumeric_error_count(self):
        ok, detail = interpret_skill_linter_success_stdout('{"errorCount": "oops"}')
        self.assertFalse(ok)
        self.assertIsNotNone(detail)
        self.assertIn("errorCount", detail)

    def test_skill_is_skill_linter_candidate_requires_skill_md_path(self):
        plugin_github = {"name": "p", "source": {"type": "github", "repo": "a/b"}, "skills": []}
        skill_bad = {"name": "s", "contract": {"source_assertions": {"skill_path": "x/readme.md"}}}
        skill_ok = {"name": "t", "contract": {"source_assertions": {"skill_path": ".claude/skills/t/SKILL.md"}}}
        self.assertFalse(skill_is_skill_linter_candidate(plugin_github, skill_bad))
        self.assertTrue(skill_is_skill_linter_candidate(plugin_github, skill_ok))

    def test_skill_is_skill_linter_candidate_rejects_invalid_ref(self):
        plugin_github = {"name": "p", "source": {"type": "github", "repo": "a/b", "ref": "-oops"}}
        skill_ok = {"name": "t", "contract": {"source_assertions": {"skill_path": ".claude/skills/t/SKILL.md"}}}
        self.assertFalse(skill_is_skill_linter_candidate(plugin_github, skill_ok))

    def test_normalize_git_ref_defaults_none_to_main(self):
        self.assertEqual("main", normalize_git_ref(None))

    def test_normalize_git_ref_rejects_option_like_ref(self):
        with self.assertRaises(ValueError):
            normalize_git_ref("-oops")

    def test_normalize_git_ref_rejects_embedded_whitespace(self):
        with self.assertRaises(ValueError):
            normalize_git_ref("feature branch")

    def test_select_touched_skill_keys_invalid_diff_base_returns_error(self):
        touched, errors = _select_touched_skill_keys(
            "registry.yaml",
            staged=False,
            diff_base="-oops",
            current_registry={"plugins": []},
        )
        self.assertEqual(set(), touched)
        self.assertTrue(errors)
        self.assertTrue(any("git ref" in error.lower() or "could not load" in error.lower()
                            for error in errors))

    def test_skill_is_skill_linter_candidate_accepts_git_type(self):
        plugin_git = {
            "name": "p",
            "source": {"type": "git", "url": "https://gitlab.example.com/t/p.git"},
        }
        skill_ok = {
            "name": "t",
            "contract": {"source_assertions": {"skill_path": ".claude/skills/t/SKILL.md"}},
        }
        self.assertTrue(skill_is_skill_linter_candidate(plugin_git, skill_ok))

    def test_skill_is_skill_linter_candidate_rejects_git_without_url(self):
        plugin_git = {"name": "p", "source": {"type": "git"}}
        skill_ok = {
            "name": "t",
            "contract": {"source_assertions": {"skill_path": ".claude/skills/t/SKILL.md"}},
        }
        self.assertFalse(skill_is_skill_linter_candidate(plugin_git, skill_ok))

    @mock.patch("scripts.run_skill_linter.subprocess.run")
    def test_run_captured_command_passes_timeout(self, run_mock):
        run_captured_command(["git", "status"], timeout_seconds=123)
        _, kwargs = run_mock.call_args
        self.assertEqual(kwargs["timeout"], 123)
        self.assertTrue(kwargs["capture_output"])
        self.assertTrue(kwargs["text"])

    @mock.patch("scripts.run_skill_linter.subprocess.run")
    def test_run_captured_command_wraps_timeout(self, run_mock):
        run_mock.side_effect = subprocess.TimeoutExpired(["git", "status"], 5)
        with self.assertRaises(RuntimeError):
            run_captured_command(["git", "status"], timeout_seconds=5)


if __name__ == "__main__":
    unittest.main()
