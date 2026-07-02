import subprocess
import unittest
from unittest import mock

from scripts.registry_contracts import (
    SkillKey,
    detect_touched_skills,
    load_registry_from_ref,
    load_staged_registry,
    source_browse_url,
    source_clone_url,
    source_display_name,
)


def build_registry():
    return {
        "name": "example-registry",
        "owner": {"name": "example-org"},
        "plugins": [
            {
                "name": "example-plugin",
                "description": "Example plugin",
                "version": "1.0.0",
                "source": {"type": "github", "repo": "example-org/example-plugin", "ref": "main"},
                "skills": [
                    {
                        "name": "example-skill",
                        "description": "Example skill",
                    },
                    {
                        "name": "example-skill-two",
                        "description": "Second skill",
                    },
                ],
            }
        ],
    }


class TouchDetectionTests(unittest.TestCase):
    def test_detects_skill_change(self):
        before = build_registry()
        after = build_registry()
        after["plugins"][0]["skills"][0]["description"] = "Updated description"

        self.assertEqual(
            [SkillKey("example-plugin", "example-skill")],
            detect_touched_skills(before, after),
        )

    def test_no_touch_when_strict_omitted_vs_explicit_true(self):
        before = build_registry()
        after = build_registry()
        after["plugins"][0]["strict"] = True

        self.assertEqual([], detect_touched_skills(before, after))

    def test_detects_plugin_source_ref_change_for_all_skills(self):
        before = build_registry()
        after = build_registry()
        after["plugins"][0]["source"]["ref"] = "stable"

        self.assertEqual(
            [
                SkillKey("example-plugin", "example-skill"),
                SkillKey("example-plugin", "example-skill-two"),
            ],
            detect_touched_skills(before, after),
        )


class RegistryGitReadTests(unittest.TestCase):
    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_load_registry_from_ref_rejects_option_like_ref(self, run_mock):
        run_mock.side_effect = AssertionError("subprocess.run should not be called")
        with self.assertRaises(ValueError):
            load_registry_from_ref("-oops")

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_load_registry_from_ref_rejects_invalid_path_token(self, run_mock):
        run_mock.side_effect = AssertionError("subprocess.run should not be called")
        with self.assertRaises(ValueError):
            load_registry_from_ref("HEAD", path="../registry.yaml")

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_load_staged_registry_rejects_invalid_path_token(self, run_mock):
        run_mock.side_effect = AssertionError("subprocess.run should not be called")
        with self.assertRaises(ValueError):
            load_staged_registry(path="../registry.yaml")

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_load_registry_from_ref_wraps_timeouts(self, run_mock):
        run_mock.side_effect = subprocess.TimeoutExpired(["git", "show"], 30)
        with self.assertRaises(RuntimeError):
            load_registry_from_ref("HEAD")

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_load_staged_registry_wraps_timeouts(self, run_mock):
        run_mock.side_effect = subprocess.TimeoutExpired(["git", "show"], 30)
        with self.assertRaises(RuntimeError):
            load_staged_registry()

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_load_registry_from_ref_passes_timeout(self, run_mock):
        run_mock.return_value = subprocess.CompletedProcess(
            ["git", "show"],
            0,
            stdout="name: example\nplugins: []\n",
            stderr="",
        )
        load_registry_from_ref("HEAD")
        _, kwargs = run_mock.call_args
        self.assertEqual(kwargs["timeout"], 30)


class SourceHelperTests(unittest.TestCase):
    def test_source_clone_url_github(self):
        source = {"type": "github", "repo": "opendatahub-io/rfe-creator"}
        self.assertEqual("https://github.com/opendatahub-io/rfe-creator.git", source_clone_url(source))

    def test_source_clone_url_git(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin.git"}
        self.assertEqual("https://gitlab.corp.example.com/team/my-plugin.git", source_clone_url(source))

    def test_source_clone_url_unsupported_type_raises(self):
        with self.assertRaises(ValueError):
            source_clone_url({"type": "npm", "repo": "foo"})

    def test_source_display_name_github(self):
        source = {"type": "github", "repo": "opendatahub-io/rfe-creator"}
        self.assertEqual("opendatahub-io/rfe-creator", source_display_name(source))

    def test_source_display_name_git_strips_scheme_and_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin.git"}
        self.assertEqual("gitlab.corp.example.com/team/my-plugin", source_display_name(source))

    def test_source_display_name_git_no_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin"}
        self.assertEqual("gitlab.corp.example.com/team/my-plugin", source_display_name(source))

    def test_source_browse_url_github(self):
        source = {"type": "github", "repo": "opendatahub-io/rfe-creator"}
        self.assertEqual("https://github.com/opendatahub-io/rfe-creator", source_browse_url(source))

    def test_source_browse_url_git_strips_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin.git"}
        self.assertEqual("https://gitlab.corp.example.com/team/my-plugin", source_browse_url(source))

    def test_source_browse_url_git_no_dotgit(self):
        source = {"type": "git", "url": "https://gitlab.corp.example.com/team/my-plugin"}
        self.assertEqual("https://gitlab.corp.example.com/team/my-plugin", source_browse_url(source))


if __name__ == "__main__":
    unittest.main()
