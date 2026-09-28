import unittest

import scripts.generate_catalog as generate_catalog

from tests.registry_contract_fixtures import build_registry_with_contract


class CatalogContractRenderingTests(unittest.TestCase):
    def test_catalog_renders_function_and_metric_columns(self):
        content = generate_catalog.generate_catalog(build_registry_with_contract())
        self.assertIn("## Canonical Contract System", content)
        self.assertIn("| Skill | Description | Functions | Metrics |", content)
        self.assertIn("`review`", content)
        self.assertIn("`task_success`", content)
        self.assertIn("deterministic", content)
        self.assertIn("judge", content)

    def test_catalog_handles_null_contract_without_crashing(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["skills"][0]["contract"] = None
        content = generate_catalog.generate_catalog(registry)
        self.assertIn("| Skill | Description |", content)
        self.assertIn("| `/example-skill` | Example skill |", content)
        self.assertNotIn("| Skill | Description | Functions | Metrics |", content)

    def test_catalog_uses_compact_table_when_plugin_has_no_contracts(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["skills"][0].pop("contract")
        content = generate_catalog.generate_catalog(registry)
        self.assertIn("| Skill | Description |", content)
        self.assertNotIn("| Skill | Description | Functions | Metrics |", content)


class CatalogGitSourceTests(unittest.TestCase):
    def test_catalog_renders_git_source_browse_link(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
        }

        content = generate_catalog.generate_catalog(registry)

        self.assertIn("[gitlab.example.com/team/plugin](https://gitlab.example.com/team/plugin)", content)
        self.assertNotIn("github.com", content.split("Quick Start")[1])


class CatalogMultilineDescriptionTests(unittest.TestCase):
    def test_multiline_skill_description_renders_single_row(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["skills"][0]["description"] = (
            "First line of the description.\nSecond line after a newline.\n"
        )

        content = generate_catalog.generate_catalog(registry)

        # The description must be collapsed onto one properly-terminated table row.
        self.assertIn(
            "First line of the description. Second line after a newline.", content)
        # The renderer appends " |", so a broken row would contain "\n |".
        self.assertNotIn("Second line after a newline.\n |", content)


class CatalogMcpServerTests(unittest.TestCase):
    def test_catalog_renders_mcp_servers_table(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["mcp_servers"] = [
            {"name": "patternfly", "description": "Component docs via MCP"}
        ]

        content = generate_catalog.generate_catalog(registry)

        self.assertIn("| MCP Server | Description |", content)
        self.assertIn("| patternfly | Component docs via MCP |", content)


class CatalogGitSubdirSourceTests(unittest.TestCase):
    def test_catalog_deep_links_into_the_subdirectory(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://github.com/acme/monorepo.git",
            "path": "plugins/thing",
            "ref": "main",
        }

        content = generate_catalog.generate_catalog(registry)

        self.assertIn(
            "[acme/monorepo/plugins/thing]"
            "(https://github.com/acme/monorepo/tree/main/plugins/thing)",
            content,
        )

    def test_catalog_links_repo_root_for_non_github_forge(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["source"] = {
            "type": "git-subdir",
            "url": "https://gitlab.example.com/team/monorepo.git",
            "path": "plugins/thing",
        }

        content = generate_catalog.generate_catalog(registry)

        # GitLab spells subdirectory browsing differently, so no deep link.
        self.assertIn("(https://gitlab.example.com/team/monorepo)", content)
        self.assertNotIn("/tree/", content)


class CatalogSkillCountTests(unittest.TestCase):
    """A plugin that delegates discovery declares a count instead of a list."""

    def _registry_with_count(self, count):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin.pop("skills", None)
        plugin["skill_count"] = count
        return registry

    def test_renders_count_when_no_skills_are_listed(self):
        content = generate_catalog.generate_catalog(self._registry_with_count(69))
        self.assertIn("**69 skills**", content)

    def test_singular_noun_for_one_skill(self):
        content = generate_catalog.generate_catalog(self._registry_with_count(1))
        self.assertIn("**1 skill**,", content)

    def test_no_count_line_for_mcp_only_plugin(self):
        content = generate_catalog.generate_catalog(self._registry_with_count(0))
        self.assertNotIn("**0 skills**", content)

    def test_listed_skills_still_render_a_table(self):
        registry = build_registry_with_contract()
        content = generate_catalog.generate_catalog(registry)
        self.assertIn("| `/example-skill` |", content)
        self.assertNotIn("discovered from the source repository", content)


class CatalogMalformedContractRenderingTests(unittest.TestCase):
    def test_catalog_skips_non_dict_contract_for_columns(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["skills"][0]["contract"] = "not-a-contract"
        content = generate_catalog.generate_catalog(registry)
        self.assertIn("| Skill | Description |", content)
        self.assertIn("| `/example-skill` | Example skill |", content)
        self.assertNotIn("| Skill | Description | Functions | Metrics |", content)
