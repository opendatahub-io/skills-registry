import os
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts.registry_contracts import (
    SkillKey,
    detect_touched_skills,
    load_registry_from_ref,
    load_staged_registry,
    redact_url,
    shallow_clone,
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


class RedactUrlTests(unittest.TestCase):
    def test_redacts_user_and_password(self):
        self.assertEqual(
            "https://***@host.example.com/x.git",
            redact_url("https://user:token@host.example.com/x.git"),
        )

    def test_redacts_bare_user(self):
        self.assertEqual(
            "https://***@host/x.git",
            redact_url("https://user@host/x.git"),
        )

    def test_preserves_url_without_userinfo(self):
        self.assertEqual(
            "https://host.example.com/x.git",
            redact_url("https://host.example.com/x.git"),
        )

    def test_redacts_credentials_in_stderr_like_text(self):
        text = "fatal: unable to access 'https://oauth2:SECRET@gitlab.com/team/x.git/': ..."
        self.assertNotIn("SECRET", redact_url(text))
        self.assertIn("https://***@gitlab.com", redact_url(text))


class ShallowCloneTests(unittest.TestCase):
    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_shallow_clone_succeeds_with_branch(self, run_mock):
        run_mock.return_value = subprocess.CompletedProcess(
            ["git", "clone"], 0, stdout="", stderr=""
        )

        result = shallow_clone("https://example.com/repo.git", "main", "/tmp/dest")

        self.assertEqual(0, result.returncode)
        run_mock.assert_called_once()
        cmd = run_mock.call_args[0][0]
        self.assertIn("--branch", cmd)
        self.assertIn("main", cmd)

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_shallow_clone_falls_back_for_sha(self, run_mock):
        sha = "a" * 40
        branch_fail = subprocess.CompletedProcess(["git", "clone"], 128, stdout="", stderr="")
        clone_ok = subprocess.CompletedProcess(["git", "clone"], 0, stdout="", stderr="")
        checkout_ok = subprocess.CompletedProcess(["git", "checkout"], 0, stdout="", stderr="")
        run_mock.side_effect = [branch_fail, clone_ok, checkout_ok]

        result = shallow_clone("https://example.com/repo.git", sha, "/tmp/dest")

        self.assertEqual(0, result.returncode)
        self.assertEqual(3, run_mock.call_count)
        # Second call is the fallback clone: it MUST be a full (non-shallow) clone,
        # otherwise a historical SHA cannot be checked out (see the integration test).
        fallback_cmd = run_mock.call_args_list[1][0][0]
        self.assertNotIn("--depth", fallback_cmd)
        # Third call should be checkout --detach <sha>
        checkout_cmd = run_mock.call_args_list[2][0][0]
        self.assertIn("--detach", checkout_cmd)
        self.assertIn(sha, checkout_cmd)

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_shallow_clone_returns_failure_when_both_fail(self, run_mock):
        fail = subprocess.CompletedProcess(["git"], 128, stdout="", stderr="fatal")
        run_mock.return_value = fail

        result = shallow_clone("https://example.com/repo.git", "main", "/tmp/dest")

        self.assertNotEqual(0, result.returncode)

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_shallow_clone_returns_failed_checkout(self, run_mock):
        sha = "b" * 40
        branch_fail = subprocess.CompletedProcess(["git", "clone"], 128, stdout="", stderr="")
        clone_ok = subprocess.CompletedProcess(["git", "clone"], 0, stdout="", stderr="")
        checkout_fail = subprocess.CompletedProcess(
            ["git", "checkout"], 1, stdout="", stderr="fatal: unable to read tree"
        )
        run_mock.side_effect = [branch_fail, clone_ok, checkout_fail]

        result = shallow_clone("https://example.com/repo.git", sha, "/tmp/dest")

        # The failed checkout is surfaced to the caller (not masked as clone success).
        self.assertEqual(3, run_mock.call_count)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("unable to read tree", result.stderr)

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_shallow_clone_raises_on_timeout(self, run_mock):
        run_mock.side_effect = subprocess.TimeoutExpired(["git"], 120)

        with self.assertRaises(RuntimeError):
            shallow_clone("https://example.com/repo.git", "main", "/tmp/dest")

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_shallow_clone_raises_on_fallback_clone_timeout(self, run_mock):
        branch_fail = subprocess.CompletedProcess(["git", "clone"], 128, stdout="", stderr="")
        run_mock.side_effect = [branch_fail, subprocess.TimeoutExpired(["git"], 120)]

        with self.assertRaises(RuntimeError):
            shallow_clone("https://example.com/repo.git", "c" * 40, "/tmp/dest")

    @mock.patch("scripts.registry_contracts.subprocess.run")
    def test_shallow_clone_raises_on_checkout_timeout(self, run_mock):
        branch_fail = subprocess.CompletedProcess(["git", "clone"], 128, stdout="", stderr="")
        clone_ok = subprocess.CompletedProcess(["git", "clone"], 0, stdout="", stderr="")
        run_mock.side_effect = [branch_fail, clone_ok, subprocess.TimeoutExpired(["git"], 120)]

        with self.assertRaises(RuntimeError):
            shallow_clone("https://example.com/repo.git", "d" * 40, "/tmp/dest")


@unittest.skipUnless(shutil.which("git"), "git is required for integration tests")
class ShallowCloneIntegrationTests(unittest.TestCase):
    """End-to-end against a real local repo (no mocks) — exercises the SHA fallback."""

    _GIT_ENV = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
    }

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True, env=self._GIT_ENV
        )

    def _make_repo(self, path: str) -> str:
        """Create a repo with three commits; return the SHA of the first (historical) one."""
        os.makedirs(path)
        self._git("init", "-q", path)
        shas = []
        for msg in ("c1", "c2", "c3"):
            self._git("-C", path, "commit", "-q", "--allow-empty", "-m", msg)
            shas.append(self._git("-C", path, "rev-parse", "HEAD").stdout.strip())
        return shas[0]  # historical commit, NOT the default-branch tip

    def test_checks_out_historical_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src")
            historical = self._make_repo(src)
            dest = os.path.join(tmp, "dest")
            # Use file:// so git honors --depth. A bare local-path clone silently
            # ignores --depth (full clone), which would mask a shallow regression.
            url = f"file://{src}"

            result = shallow_clone(url, historical, dest)

            self.assertEqual(0, result.returncode, result.stderr)
            head = subprocess.run(
                ["git", "-C", dest, "rev-parse", "HEAD"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            self.assertEqual(historical, head)

    def test_checks_out_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src")
            self._make_repo(src)
            branch = self._git("-C", src, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
            dest = os.path.join(tmp, "dest")

            result = shallow_clone(f"file://{src}", branch, dest)

            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
