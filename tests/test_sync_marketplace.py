import unittest

import scripts.sync_marketplace as sync_marketplace


class SourceTypeMappingTests(unittest.TestCase):
    """Verify that registry source types map to correct marketplace source types."""

    def _make_plugin(self, source):
        return {
            "name": "test-plugin",
            "description": "A test plugin",
            "version": "1.0.0",
            "source": source,
        }

    def test_github_source_maps_to_github(self):
        plugin = self._make_plugin({
            "type": "github",
            "repo": "opendatahub-io/test-repo",
            "ref": "main",
        })
        entry = sync_marketplace.plugin_to_marketplace_entry(plugin)
        self.assertEqual(entry["source"]["source"], "github")

    def test_git_source_maps_to_url(self):
        plugin = self._make_plugin({
            "type": "git",
            "url": "https://gitlab.example.com/team/repo.git",
            "ref": "main",
        })
        entry = sync_marketplace.plugin_to_marketplace_entry(plugin)
        self.assertEqual(entry["source"]["source"], "url")

    def test_git_source_preserves_url_field(self):
        clone_url = "https://gitlab.example.com/team/repo.git"
        plugin = self._make_plugin({
            "type": "git",
            "url": clone_url,
            "ref": "main",
        })
        entry = sync_marketplace.plugin_to_marketplace_entry(plugin)
        self.assertEqual(entry["source"]["url"], clone_url)


class SkillsDirWithEitherStrictTests(unittest.TestCase):
    """The entry's ``skills`` come from ``skills_dir`` whatever ``strict`` says: with
    ``strict: true`` Claude Code appends them to the repo's ``plugin.json``, and a repo
    that has no manifest yet is defined by the entry either way."""

    def _plugin(self, **extra):
        return {"name": "p", "source": {"type": "github", "repo": "o/r"}, **extra}

    def test_strict_true_keeps_skills_and_omits_strict(self):
        entry = sync_marketplace.plugin_to_marketplace_entry(
            self._plugin(strict=True, skills_dir=".claude/skills"))
        self.assertEqual(["./.claude/skills"], entry["skills"])
        self.assertNotIn("strict", entry)

    def test_strict_false_keeps_skills_and_strict(self):
        entry = sync_marketplace.plugin_to_marketplace_entry(
            self._plugin(strict=False, skills_dir=".claude/skills"))
        self.assertEqual(["./.claude/skills"], entry["skills"])
        self.assertIs(False, entry["strict"])

    def test_no_skills_dir_emits_no_skills(self):
        entry = sync_marketplace.plugin_to_marketplace_entry(self._plugin())
        self.assertNotIn("skills", entry)
