import unittest
from collections import OrderedDict

from main.dicts.enrichers_dict import get_enricher_dict
from main.enrichers.ad_enricher import AdEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.dns_lookup_enricher import DnsLookupEnricher
from main.enrichers.ip_address_combine_enricher import IpAddressCombineEnricher
from main.enrichers.ip_type_enricher import IpTypeEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.server_type_enricher import ServerTypeEnricher
from main.enrichers.stream_enricher import StreamEnricher
from main.enrichers.threat_info_enricher import ThreatInfoEnricher
from main.enrichers.tls_enricher import TlsEnricher


class TestEnrichmentClassesMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.enricher_keys = [
            "ip_address_combine_enricher",
            "location_enricher",
            "fqdn_resolve_enricher",
            "stream_enricher",
            "tls_ssl_version_enricher",
            "cipher_suite_enricher",
            "ip_type_enricher",
            "dns_lookup_enricher",
            "server_type_enricher",
            "ad_enricher",
            "threat_info_enricher"
        ]

    def setUp(self) -> None:
        self.enricher_dict = get_enricher_dict()

    def test_create_enrichers_classes(self) -> None:
        for key in self.enricher_dict:
            if key == "ip_address_combine_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], IpAddressCombineEnricher))

            elif key == "location_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], LocationEnricher))

            elif key == "fqdn_resolve_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], NameResolverEnricher))

            elif key == "cipher_suite_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], CipherSuiteEnricher))

            elif key == "tls_ssl_version_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], TlsEnricher))

            elif key == "ip_type_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], IpTypeEnricher))

            elif key == "stream_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], StreamEnricher))

            elif key == "dns_lookup_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], DnsLookupEnricher))

            elif key == "server_type_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], ServerTypeEnricher))

            elif key == "ad_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], AdEnricher))

            elif key == "threat_info_enricher":
                self.assertTrue(isinstance(self.enricher_dict[key], ThreatInfoEnricher))
            else:
                self.assertTrue(False)

    def test_create_enrichers_is_dict(self) -> None:
        self.assertTrue(isinstance(self.enricher_dict, OrderedDict))

    def test_create_enrichers_keys(self) -> None:
        self.assertEqual(list(self.enricher_dict), self.enricher_keys)

    def test_enricher_dict_keys(self) -> None:
        self.assertListEqual(list(self.enricher_dict), self.enricher_keys)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichmentClassesMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
