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


if __name__ == "__main__":
    unittest.main()
