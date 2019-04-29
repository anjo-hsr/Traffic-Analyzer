import unittest

from main.enrichers.location_enricher import LocationEnricher


class TestLocationEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.location_enricher = LocationEnricher()
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
                "rdns": "8.8.8.8",
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
        expected_header = "dst_latitude,dst_longitude,src_latitude,src_longitude"
        self.assertEqual(self.location_enricher.header, expected_header)

    def test_extract_location_local_connection(self):
        locations = self.location_enricher.extract_location(self.dst_src_information_local)
        empty_location = '"","","",""'
        self.assertEqual(locations, empty_location)

    def test_extract_location_public_connection(self):
        locations = self.location_enricher.extract_location(self.dst_src_information_public)
        expected_fqnds = '"37.751","-97.822","",""'
        self.assertEqual(locations, expected_fqnds)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocationEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
