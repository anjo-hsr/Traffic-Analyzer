import unittest
from collections import OrderedDict

from main.enricher_jar import EnricherJar


class TestEnricherJarMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.enricher_jar = EnricherJar()

    def test_create_information_dict(self) -> None:
        packet = {
            "ip.dst": "10.0.0.2",
            "ip.src": "10.0.0.1",
            "ipv6.dst": "",
            "ipv6.src": ""
        }
        expected_ordered_dict = OrderedDict([
            ('dst_src_information',
             {
                 'dst': {
                     'asn': '',
                     'ip_address': '10.0.0.2',
                     'isp': '',
                     'latitude': '',
                     'longitude': '',
                     'rdns': '10.0.0.2'
                 },
                 'src': {
                     'asn': '',
                     'ip_address': '10.0.0.1',
                     'isp': '',
                     'latitude': '',
                     'longitude': '',
                     'rdns': '10.0.0.1'
                 }
             }
             )
        ])

        information_dict = self.enricher_jar.create_information_dict(packet)
        self.assertEqual(information_dict, expected_ordered_dict)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnricherJarMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
