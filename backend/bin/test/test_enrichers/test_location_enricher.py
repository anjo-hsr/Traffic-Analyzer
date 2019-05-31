import unittest

from main.enrichers.location_enricher import LocationEnricher


class TestLocationEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.location_enricher = LocationEnricher()
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
        }

    def test_header(self) -> None:
        expected_header = "dst_latitude,dst_longitude,src_latitude,src_longitude"
        self.assertEqual(self.location_enricher.header, expected_header)

    def test_extract_location_local_connection(self) -> None:
        self.location_enricher.get_information(self.packet, self.information_dict_local)
        empty_location = '""'

        self.assertEqual(self.information_dict_local["dst_latitude"], empty_location)
        self.assertEqual(self.information_dict_local["dst_longitude"], empty_location)
        self.assertEqual(self.information_dict_local["src_latitude"], empty_location)
        self.assertEqual(self.information_dict_local["src_longitude"], empty_location)

    def test_extract_location_public_connection(self) -> None:
        self.location_enricher.get_information(self.packet, self.information_dict_public)
        expected_dst_latitude = '"37.751"'
        expected_dst_longitude = '"-97.822"'
        expected_src_latitude = '""'
        expected_src_longitude = '""'

        self.assertEqual(self.information_dict_public["dst_latitude"], expected_dst_latitude)
        self.assertEqual(self.information_dict_public["dst_longitude"], expected_dst_longitude)
        self.assertEqual(self.information_dict_public["src_latitude"], expected_src_latitude)
        self.assertEqual(self.information_dict_public["src_longitude"], expected_src_longitude)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocationEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
