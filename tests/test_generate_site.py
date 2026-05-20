import unittest

import scripts.generate_site as generate_site

from tests.registry_contract_fixtures import build_registry_with_contract


class SiteContractRenderingTests(unittest.TestCase):
    def test_skill_page_renders_contract_section(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        skill = plugin["skills"][0]

        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)

        self.assertIn("## Contract", page)
        self.assertIn("canonical-skill-v1", page)
        self.assertIn("task_success", page)
        self.assertIn("`review`", page)
        self.assertIn("### Problem Statement", page)
        self.assertIn("### Success Conditions", page)
        self.assertIn("### Metrics", page)
        self.assertIn("`judge`", page)
        self.assertIn("example-org/example-plugin@main:docs/review-rubric.md", page)
        self.assertIn("### Invariants", page)
        self.assertIn("### Source Assertions", page)
        self.assertIn("skills/example-skill/SKILL.md", page)
        idx_contract = page.index("## Contract")
        idx_review = page.index("`review`", idx_contract)
        self.assertGreater(idx_review, idx_contract)

    def test_skill_page_omits_contract_when_contract_is_not_mapping(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        skill = plugin["skills"][0]
        skill["contract"] = None
        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract", page)

        skill["contract"] = ["oops"]
        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract", page)

    def test_plugin_page_renders_contract_summary(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin["contract_summary"] = {
            "focus_functions": ["review"],
            "focus_metrics": ["task_success"],
            "notes": "Example summary",
        }

        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)

        self.assertIn("## Contract Summary", page)
        self.assertIn("Example summary", page)

    def test_plugin_page_skips_non_mapping_contract_summary(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin["contract_summary"] = None
        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract Summary", page)

        plugin["contract_summary"] = "invalid"
        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract Summary", page)
