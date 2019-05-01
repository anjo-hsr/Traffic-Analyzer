import unittest
from collections import OrderedDict

from main.enrichers.ad_enricher import AdEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.dns_lookup_enricher import DnsLookupEnricher
from main.enrichers.ip_type_enricher import IpTypeEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.stream_enricher import StreamEnricher
from main.enrichers.tls_enricher import TlsEnricher
from main.enricher import Enricher


class TestEnrichmentClassesMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enrichment_classes = Enricher()

    def setUp(self):
        self.enrichment_classes.reset_variables()

    def test_create_enrichers_classes(self):
        enrichers = self.enrichment_classes.enrichers

        for key in enrichers.keys():
            if key == "location_enricher":
                self.assertTrue(isinstance(enrichers[key], LocationEnricher))

            elif key == "name_resolve_enricher":
                self.assertTrue(isinstance(enrichers[key], NameResolverEnricher))

            elif key == "cipher_suite_enricher":
                self.assertTrue(isinstance(enrichers[key], CipherSuiteEnricher))

            elif key == "tls_ssl_version_enricher":
                self.assertTrue(isinstance(enrichers[key], TlsEnricher))

            elif key == "ip_type_enricher":
                self.assertTrue(isinstance(enrichers[key], IpTypeEnricher))

            elif key == "stream_enricher":
                self.assertTrue(isinstance(enrichers[key], StreamEnricher))

            elif key == "ad_enricher":
                self.assertTrue(isinstance(enrichers[key], AdEnricher))

            elif key == "dns_lookup_enricher":
                self.assertTrue(isinstance(enrichers[key], DnsLookupEnricher))

            else:
                self.assertTrue(False)

    def test_create_enrichers_is_dict(self):
        enrichers = self.enrichment_classes.enrichers
        self.assertTrue(isinstance(enrichers, OrderedDict))

    def test_create_enrichers_keys(self):
        test_keys = [
            "location_enricher",
            "name_resolve_enricher",
            "cipher_suite_enricher",
            "tls_ssl_version_enricher",
            "ip_type_enricher",
            "stream_enricher",
            "ad_enricher",
            "dns_lookup_enricher"
        ]

        enrichers = self.enrichment_classes.enrichers
        keys = [enricher_key for enricher_key in enrichers]
        self.assertEqual(keys, test_keys)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichmentClassesMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
