import unittest

import main.enrich_csv as add_information
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.protocol_enricher import ProtocolEnricher
from main.enrichers.tls_enricher import TlsEnricher


class TestEnrichCsv(unittest.TestCase):
    def test_create_helpers_classes(self):
        helpers = add_information.create_enrichers()
        keys = helpers.keys()

        for key in keys:
            if key == "location_enricher":
                self.assertTrue(isinstance(helpers[key], LocationEnricher))

            elif key == "name_resolve_enricher":
                self.assertTrue(isinstance(helpers[key], NameResolverEnricher))

            elif key == "cipher_suite_enricher":
                self.assertTrue(isinstance(helpers[key], CipherSuiteEnricher))

            elif key == "tls_ssl_version_enricher":
                self.assertTrue(isinstance(helpers[key], TlsEnricher))

            elif key == "protocol_enricher":
                self.assertTrue(isinstance(helpers[key], ProtocolEnricher))

            else:
                self.assertTrue(False)

    def test_create_helpers_is_dict(self):
        helpers = add_information.create_enrichers()
        self.assertTrue(isinstance(helpers, dict))

    def test_create_helpers_keys(self):
        test_keys = ["location_enricher", "name_resolve_enricher", "cipher_suite_enricher", "tls_ssl_version_enricher", "protocol_enricher"]

        helpers = add_information.create_enrichers()
        keys = [helper_key for helper_key in helpers]
        self.assertListEqual(keys, test_keys)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichCsv)
    unittest.TextTestRunner(verbosity=2).run(suite)
