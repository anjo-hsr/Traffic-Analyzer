import unittest
from collections import OrderedDict

import main.enrich_csv as add_information
from main.enrichers.ad_enricher import AdEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.tls_enricher import TlsEnricher


class TestEnrichCsv(unittest.TestCase):
    def test_create_enrichers_classes(self):
        enrichers = add_information.create_enrichers()
        keys = enrichers.keys()

        for key in keys:
            if key == "location_enricher":
                self.assertTrue(isinstance(enrichers[key], LocationEnricher))

            elif key == "name_resolve_enricher":
                self.assertTrue(isinstance(enrichers[key], NameResolverEnricher))

            elif key == "cipher_suite_enricher":
                self.assertTrue(isinstance(enrichers[key], CipherSuiteEnricher))

            elif key == "tls_ssl_version_enricher":
                self.assertTrue(isinstance(enrichers[key], TlsEnricher))

            elif key == "ad_enricher":
                self.assertTrue(isinstance(enrichers[key], AdEnricher))

            else:
                self.assertTrue(False)

    def test_create_enrichers_is_dict(self):
        enrichers = add_information.create_enrichers()
        self.assertTrue(isinstance(enrichers, OrderedDict))

    def test_create_enrichers_keys(self):
        test_keys = [
            "location_enricher",
            "name_resolve_enricher",
            "cipher_suite_enricher",
            "tls_ssl_version_enricher",
            "ad_enricher"
        ]

        enrichers = add_information.create_enrichers()
        keys = [enricher_key for enricher_key in enrichers]
        self.assertEqual(keys, test_keys)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichCsv)
    unittest.TextTestRunner(verbosity=2).run(suite)
