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
