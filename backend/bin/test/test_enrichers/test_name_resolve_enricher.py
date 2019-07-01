import unittest

from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.helpers.string_helper import enclose_with_quotes


class TestNameResolveEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.name_resolver_enricher = NameResolverEnricher()
        cls.packet = {}
        cls.information_dict_local = {
            "dst_src_information": {
                "dst": {
                    "rdns": "10.0.0.1",
                    "asn": "",
                    "isp": "",
                    "latitude": "",
                    "longitude": ""
                },
                "src": {
                    "rdns": "10.0.0.2",
                    "asn": "",
                    "isp": "",
                    "latitude": "",
                    "longitude": ""
                }
            }
        }
        cls.information_dict_public = {
            "dst_src_information": {
                "dst": {
                    "rdns": "dns.google",
                    "asn": "15169",
                    "isp": "Google LLC",
                    "latitude": "37.751",
                    "longitude": "-97.822"
                },
                "src": {
                    "rdns": "10.0.0.1",
                    "asn": "",
                    "isp": "",
                    "latitude": "",
                    "longitude": ""
                }
            }
        }

    def test_header(self) -> None:
        expected_header = "dst_fqdn,src_fqdn"
        self.assertEqual(self.name_resolver_enricher.header, expected_header)

    def test_extract_location_local_connection(self) -> None:
        self.name_resolver_enricher.get_information(self.packet, self.information_dict_local)
        dst_fqdns = enclose_with_quotes("10.0.0.1")
        src_fqdns = enclose_with_quotes("10.0.0.2")
        self.assertEqual(self.information_dict_local["dst_fqdn"], dst_fqdns)
        self.assertEqual(self.information_dict_local["src_fqdn"], src_fqdns)

    def test_extract_location_public_connection(self) -> None:
        self.name_resolver_enricher.get_information(self.packet, self.information_dict_public)
        dst_fqdns = enclose_with_quotes("dns.google")
        src_fqdns = enclose_with_quotes("10.0.0.1")
        self.assertEqual(self.information_dict_public["dst_fqdn"], dst_fqdns)
        self.assertEqual(self.information_dict_public["src_fqdn"], src_fqdns)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNameResolveEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
