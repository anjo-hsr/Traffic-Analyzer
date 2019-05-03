import unittest
from collections import OrderedDict

from main.enricher import Enricher
from main.enrichers.ad_enricher import AdEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.dns_lookup_enricher import DnsLookupEnricher
from main.enrichers.ip_type_enricher import IpTypeEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.stream_enricher import StreamEnricher
from main.enrichers.tls_enricher import TlsEnricher


class TestEnrichmentClassesMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enricher = Enricher()
        cls.test_keys = [
            "location_enricher",
            "fqdn_resolve_enricher",
            "cipher_suite_enricher",
            "tls_ssl_version_enricher",
            "ip_type_enricher",
            "stream_enricher",
            "ad_enricher",
            "dns_lookup_enricher"
        ]

    def setUp(self):
        self.enricher.reset_variables()

    def test_create_enrichers_classes(self):
        enrichers_dict = self.enricher.enricher_classes.enrichers_dict

        for key in enrichers_dict.keys():
            if key == "location_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], LocationEnricher))

            elif key == "fqdn_resolve_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], NameResolverEnricher))

            elif key == "cipher_suite_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], CipherSuiteEnricher))

            elif key == "tls_ssl_version_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], TlsEnricher))

            elif key == "ip_type_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], IpTypeEnricher))

            elif key == "stream_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], StreamEnricher))

            elif key == "dns_lookup_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], DnsLookupEnricher))

            elif key == "ad_enricher":
                self.assertTrue(isinstance(enrichers_dict[key], AdEnricher))


            else:
                self.assertTrue(False)

    def test_create_enrichers_is_dict(self):
        enrichers_dict = self.enricher.enricher_classes.enrichers_dict
        self.assertTrue(isinstance(enrichers_dict, OrderedDict))

    def test_create_enrichers_keys(self):
        enrichers_dict = self.enricher.enricher_classes.enrichers_dict
        self.assertEqual(list(enrichers_dict.keys()), self.test_keys)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichmentClassesMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
