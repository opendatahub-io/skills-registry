import unittest

import scripts.generate_catalog as generate_catalog

from tests.registry_contract_fixtures import build_registry_with_contract


class CatalogContractRenderingTests(unittest.TestCase):
    def test_catalog_renders_function_and(self):
        content = generate_catalog.generate_catalog(build_registry_with_contract())
        self.assertIn("## Canonical Contract System", content)
        self.assertIn("| Skill | Description | Functions | Metrics |", content)
        self.assertIn("`review`", content)
        self.assertIn("`task_success`", content)
        self.assertIn("deterministic", content)
        self.assertIn("judge", content)

    def test_catalog_handles_null_contract(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["skills"][0]["contract"] = None
        content = generate_catalog.generate_catalog(registry)
        self.assertIn("| Skill | Description |", content)
        self.assertIn("| `/example-skill` | Example skill |", content)
        self.assertNotIn("| Skill | Description | Functions | Metrics |", content)

    def test_catalog_uses_compact_table_when_plugin_has(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["skills"][0].pop("contract")
        content = generate_catalog.generate_catalog(registry)
        self.assertIn("| Skill | Description |", content)
        self.assertNotIn("| Skill | Description | Functions | Metrics |", content)


class CatalogMalformedContractRenderingTests(unittest.TestCase):
    def test_catalog_skips_non_dict_contract(self):
        registry = build_registry_with_contract()
        registry["plugins"][0]["skills"][0]["contract"] = "not-a-contract"
        content = generate_catalog.generate_catalog(registry)
        self.assertIn("| Skill | Description |", content)
        self.assertIn("| `/example-skill` | Example skill |", content)
        self.assertNotIn("| Skill | Description | Functions | Metrics |", content)
