import os
import shutil
import subprocess
import tempfile
import unittest

from scripts.discover_skills import discover_git_skills, parse_frontmatter


class ParseFrontmatterTests(unittest.TestCase):
    def test_parses_name_and_description(self):
        fm = parse_frontmatter("---\nname: foo\ndescription: does foo\n---\n# body\n")
        self.assertEqual("foo", fm["name"])
        self.assertEqual("does foo", fm["description"])

    def test_returns_empty_without_frontmatter(self):
        self.assertEqual({}, parse_frontmatter("# just a heading\n"))


@unittest.skipUnless(shutil.which("git"), "git is required for integration tests")
class DiscoverGitSkillsIntegrationTests(unittest.TestCase):
    _GIT_ENV = {
        **os.environ,
        "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
    }

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True, env=self._GIT_ENV
        )

    def _add_skill(self, src: str, name: str, body: str) -> None:
        skill_dir = os.path.join(src, "skills", name)
        os.makedirs(skill_dir)
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write(body)

    def test_discovers_skills_from_clone(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src")
            os.makedirs(src)
            self._git("init", "-q", src)
            self._add_skill(src, "alpha", "---\nname: alpha\ndescription: the alpha skill\n---\n")
            self._add_skill(
                src, "beta",
                "---\nname: beta\ndescription: the beta skill\nuser-invocable: false\n---\n",
            )
            self._git("-C", src, "add", "-A")
            self._git("-C", src, "commit", "-q", "-m", "add skills")
            # Resolve the real branch name: `git clone --branch HEAD` treats HEAD
            # as a literal ref, not the default-branch alias.
            branch = self._git("-C", src, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

            skills = discover_git_skills(f"file://{src}", branch)

            self.assertEqual(["alpha", "beta"], [s["name"] for s in skills])
            self.assertEqual("the alpha skill", skills[0]["description"])
            self.assertTrue(skills[0]["user-invocable"])
            self.assertFalse(skills[1]["user-invocable"])

    def test_returns_empty_on_clone_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = f"file://{os.path.join(tmp, 'does-not-exist')}"
            self.assertEqual([], discover_git_skills(missing, "main"))


if __name__ == "__main__":
    unittest.main()
