import unittest

import main.enrich_csv as add_information
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.tls_enricher import TlsEnricher


class TestEnrichCsv(unittest.TestCase):
    def test_create_helpers_classes(self):
        helpers = add_information.create_helpers()
        keys = helpers.keys()

        for key in keys:
            if key == "locator":
                self.assertTrue(isinstance(helpers[key], LocationEnricher))

            elif key == "name_resolver":
                self.assertTrue(isinstance(helpers[key], NameResolverEnricher))

            elif key == "cipher_suites":
                self.assertTrue(isinstance(helpers[key], CipherSuiteEnricher))

            elif key == "tls_ssl_version":
                self.assertTrue(isinstance(helpers[key], TlsEnricher))

            else:
                self.assertTrue(False)

    def test_create_helpers_is_dict(self):
        helpers = add_information.create_helpers()
        self.assertTrue(isinstance(helpers, dict))

    def test_create_helpers_keys(self):
        test_keys = ["locator", "name_resolver", "cipher_suites", "tls_ssl_version"]

        helpers = add_information.create_helpers()
        keys = [helper_key for helper_key in helpers]
        self.assertListEqual(keys, test_keys)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichCsv)
    unittest.TextTestRunner(verbosity=2).run(suite)
