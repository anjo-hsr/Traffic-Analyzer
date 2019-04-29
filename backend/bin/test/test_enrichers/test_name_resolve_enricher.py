import unittest

from main.enrichers.name_resolve_enricher import NameResolverEnricher


class TestNameResolveEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name_resolver_enricher = NameResolverEnricher()
        cls.dst_src_information_local = {
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
        cls.dst_src_information_public = {
            "dst": {
                "rdns": "google-public-dns-a.google.com",
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

    def test_header(self):
        expected_header = "dst_fqdn,src_fqdn"
        self.assertEqual(self.name_resolver_enricher.header, expected_header)

    def test_extract_location_local_connection(self):
        fqdns = self.name_resolver_enricher.extract_fqdn(self.dst_src_information_local)
        empty_fqdns = '"10.0.0.1","10.0.0.2"'
        self.assertEqual(fqdns, empty_fqdns)

    def test_extract_location_public_connection(self):
        fqdns = self.name_resolver_enricher.extract_fqdn(self.dst_src_information_public)
        expected_fqdns = '"google-public-dns-a.google.com","10.0.0.1"'
        self.assertEqual(fqdns, expected_fqdns)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNameResolveEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
