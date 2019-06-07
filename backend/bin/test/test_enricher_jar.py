import unittest
from collections import OrderedDict

from main.enricher_jar import EnricherJar
from main.helpers.domain_dict_helper import DomainDictHelper


class TestEnricherJarMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.enricher_jar = EnricherJar()
        cls.packet = {
            "ip.dst": "10.0.0.2",
            "ip.src": "10.0.0.1",
            "ipv6.dst": "",
            "ipv6.src": ""
        }

    def test_create_information_dict_dicts(self) -> None:
        key = "domain_dict_helpers"
        expected_ordered_dict = OrderedDict([
            (key, ["cdn", "social_network"])
        ])
        information_dict = self.enricher_jar.create_information_dict(self.packet)

        self.assertTrue(key in information_dict)
        for server_type in expected_ordered_dict[key]:
            self.assertTrue(isinstance(information_dict[key][server_type], DomainDictHelper))

    def test_create_information_dict_ip_information(self) -> None:
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

        information_dict = self.enricher_jar.create_information_dict(self.packet)
        for key in expected_ordered_dict:
            self.assertTrue(key in information_dict)
            self.assertTrue(information_dict[key], expected_ordered_dict[key])


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnricherJarMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
