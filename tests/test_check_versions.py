import json
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts.check_versions import fetch_remote_version_via_clone


class FetchRemoteVersionViaCloneTests(unittest.TestCase):
    @mock.patch("scripts.check_versions.subprocess.run")
    def test_returns_none_on_clone_failure(self, run_mock):
        run_mock.return_value = mock.Mock(returncode=1)

        result = fetch_remote_version_via_clone("https://example.com/repo.git", "main")

        self.assertIsNone(result)

    @mock.patch("scripts.check_versions.subprocess.run")
    def test_returns_version_from_cloned_plugin_json(self, run_mock):
        import json
        import tempfile
        from pathlib import Path

        # Create a real temp dir with plugin.json so the function can read it
        real_tmpdir = tempfile.mkdtemp()
        plugin_dir = Path(real_tmpdir) / ".claude-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "plugin.json").write_text(json.dumps({"version": "2.0.0"}))

        # Make subprocess.run succeed, and patch tempfile to return our dir
        run_mock.return_value = mock.Mock(returncode=0)

        with mock.patch("scripts.check_versions.tempfile.TemporaryDirectory") as td_mock:
            td_mock.return_value.__enter__ = mock.Mock(return_value=real_tmpdir)
            td_mock.return_value.__exit__ = mock.Mock(return_value=False)

            result = fetch_remote_version_via_clone("https://example.com/repo.git", "main")

        self.assertEqual("2.0.0", result)

        # Clean up
        import shutil
        shutil.rmtree(real_tmpdir, ignore_errors=True)


class CheckVersionsMainLoopTests(unittest.TestCase):
    """Test that the main loop dispatches correctly for git vs github types."""

    @mock.patch("scripts.check_versions.fetch_remote_version_via_clone")
    @mock.patch("scripts.check_versions.load_registry")
    def test_git_type_calls_clone_based_version_check(self, load_mock, clone_mock):
        load_mock.return_value = {
            "plugins": [{
                "name": "git-plugin",
                "version": "1.0.0",
                "source": {
                    "type": "git",
                    "url": "https://gitlab.example.com/team/plugin.git",
                    "ref": "main",
                },
            }],
        }
        clone_mock.return_value = "1.0.0"

        from scripts.check_versions import main
        with mock.patch("sys.argv", ["check_versions.py", "--dry-run"]):
            main()

        clone_mock.assert_called_once_with(
            "https://gitlab.example.com/team/plugin.git", "main"
        )

    @mock.patch("scripts.check_versions.fetch_remote_version")
    @mock.patch("scripts.check_versions.load_registry")
    def test_github_type_calls_api_based_version_check(self, load_mock, api_mock):
        load_mock.return_value = {
            "plugins": [{
                "name": "gh-plugin",
                "version": "1.0.0",
                "source": {
                    "type": "github",
                    "repo": "org/repo",
                    "ref": "main",
                },
            }],
        }
        api_mock.return_value = "1.0.0"

        from scripts.check_versions import main
        with mock.patch("sys.argv", ["check_versions.py", "--dry-run"]):
            main()

        api_mock.assert_called_once_with("org/repo", "main")


class GitSubdirAndStrictFalseTests(unittest.TestCase):
    """The sync reads the manifest Claude Code reads: at the plugin root inside the
    clone for git-subdir sources, and for strict: false plugins too when they ship one."""

    @staticmethod
    def _tree(manifests: dict[str, str]) -> str:
        real_tmpdir = tempfile.mkdtemp()
        for rel, version in manifests.items():
            d = os.path.join(real_tmpdir, rel, ".claude-plugin") if rel else os.path.join(real_tmpdir, ".claude-plugin")
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "plugin.json"), "w") as f:
                json.dump({"version": version}, f)
        return real_tmpdir

    def _via_clone(self, tree: str, **kwargs):
        with mock.patch("scripts.check_versions.subprocess.run", return_value=mock.Mock(returncode=0)), \
                mock.patch("scripts.check_versions.tempfile.TemporaryDirectory") as td_mock:
            td_mock.return_value.__enter__ = mock.Mock(return_value=tree)
            td_mock.return_value.__exit__ = mock.Mock(return_value=False)
            try:
                return fetch_remote_version_via_clone("https://example.com/repo.git", "main", **kwargs)
            finally:
                shutil.rmtree(tree, ignore_errors=True)

    def test_subdir_manifest_wins_over_the_repo_root_one(self):
        tree = self._tree({"": "9.9.9", "plugins/a": "1.0.0"})
        self.assertEqual("1.0.0", self._via_clone(tree, subdir="plugins/a"))

    def test_missing_subdir_manifest_is_none_even_with_a_root_one(self):
        tree = self._tree({"": "9.9.9"})
        self.assertIsNone(self._via_clone(tree, subdir="plugins/a"))

    def test_subdir_escaping_the_clone_is_none(self):
        tree = self._tree({"": "9.9.9"})
        self.assertIsNone(self._via_clone(tree, subdir="../elsewhere"))

    @mock.patch("scripts.check_versions.fetch_remote_version_via_clone")
    @mock.patch("scripts.check_versions.load_registry")
    def test_git_subdir_type_passes_the_subdir(self, load_mock, clone_mock):
        load_mock.return_value = {"plugins": [{
            "name": "pf-a", "version": "0.1.0",
            "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "plugins/a", "ref": "main"},
        }]}
        clone_mock.return_value = "0.1.0"
        from scripts.check_versions import main
        with mock.patch("sys.argv", ["check_versions.py", "--dry-run"]):
            main()
        clone_mock.assert_called_once_with("https://x/y.git", "main", subdir="plugins/a")

    @mock.patch("scripts.check_versions.fetch_remote_version")
    @mock.patch("scripts.check_versions.load_registry")
    def test_strict_false_plugin_is_checked_too(self, load_mock, api_mock):
        load_mock.return_value = {"plugins": [{
            "name": "loose", "version": "0.1.0", "strict": False,
            "source": {"type": "github", "repo": "org/repo", "ref": "main"},
        }]}
        api_mock.return_value = "0.1.0"
        from scripts.check_versions import main
        with mock.patch("sys.argv", ["check_versions.py", "--dry-run"]):
            main()
        api_mock.assert_called_once_with("org/repo", "main")


@unittest.skipUnless(shutil.which("git"), "git is required for integration tests")
class FetchRemoteVersionViaCloneIntegrationTests(unittest.TestCase):
    """End-to-end against a real repo — exercises shallow_clone's SHA fallback."""

    _GIT_ENV = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
    }

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True, env=self._GIT_ENV
        )

    def _write_plugin_json(self, src: str, version: str) -> None:
        os.makedirs(os.path.join(src, ".claude-plugin"), exist_ok=True)
        with open(os.path.join(src, ".claude-plugin", "plugin.json"), "w") as f:
            json.dump({"name": "p", "version": version}, f)

    def test_reads_version_at_historical_sha_and_tip(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src")
            os.makedirs(src)
            self._git("init", "-q", src)
            self._write_plugin_json(src, "1.0.0")
            self._git("-C", src, "add", "-A")
            self._git("-C", src, "commit", "-q", "-m", "v1")
            historical = self._git("-C", src, "rev-parse", "HEAD").stdout.strip()
            self._write_plugin_json(src, "2.0.0")
            self._git("-C", src, "commit", "-aq", "-m", "v2")
            branch = self._git("-C", src, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

            url = f"file://{src}"
            # Historical SHA drives the --branch-fails -> full-clone -> checkout path.
            self.assertEqual("1.0.0", fetch_remote_version_via_clone(url, historical))
            # Branch ref uses the shallow --branch path.
            self.assertEqual("2.0.0", fetch_remote_version_via_clone(url, branch))


if __name__ == "__main__":
    unittest.main()
