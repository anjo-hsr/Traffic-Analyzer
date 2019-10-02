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
from main.enrichers.tls_established_enricher import TlsEstablishedEnricher
from main.enrichers.tls_version_enricher import TlsVersionEnricher


class TestEnrichmentClassesMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.enricher_types = {
            "ip_address_combine_enricher": IpAddressCombineEnricher(),
            "location_enricher": LocationEnricher(),
            "fqdn_resolve_enricher": NameResolverEnricher(),
            "stream_enricher": StreamEnricher(),
            "tls_ssl_version_enricher": TlsVersionEnricher(),
            "tls_established_enricher": TlsEstablishedEnricher(),
            "cipher_suite_enricher": CipherSuiteEnricher(),
            "ip_type_enricher": IpTypeEnricher(),
            "dns_lookup_enricher": DnsLookupEnricher(),
            "server_type_enricher": ServerTypeEnricher(),
            "ad_enricher": AdEnricher(),
            "threat_info_enricher": ThreatInfoEnricher()
        }

    def setUp(self) -> None:
        self.enricher_dict = get_enricher_dict()

    def test_create_enrichers_classes(self) -> None:
        for key in self.enricher_dict:
            if key in self.enricher_types.keys():
                self.assertTrue(isinstance(self.enricher_dict[key], self.enricher_types[key].__class__))

            else:
                self.fail()

    def test_create_enrichers_is_dict(self) -> None:
        self.assertTrue(isinstance(self.enricher_dict, OrderedDict))

    def test_create_enrichers_keys(self) -> None:
        self.assertEqual(list(self.enricher_dict), list(self.enricher_types))

    def test_enricher_dict_keys(self) -> None:
        self.assertListEqual(list(self.enricher_dict), list(self.enricher_types))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrichmentClassesMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
