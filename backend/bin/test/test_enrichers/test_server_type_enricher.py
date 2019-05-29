import unittest

from main.enrichers.server_type_enricher import ServerTypeEnricher
from main.helpers.response_helper import ResponseHelper


class TestServerTypeEnricher(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server_type_enricher = ServerTypeEnricher()
        cls.dhcp_packet = {
            "ip.src": "10.0.0.1",
            "ip.dst": "10.0.0.2",
            "_ws.col.Protocol": "DHCP",
            "dhcp.option.dhcp": "2",
        }
        cls.dns_packet = {
            "ip.src": "10.0.0.2",
            "ip.dst": "8.8.8.8",
            "_ws.col.Protocol": "DNS",
            "dns.flags.response": "1",
        }
        cls.normal_packet = {
            "ip.src": "10.0.0.2",
            "ip.dst": "152.96.36.100",
            "_ws.col.Protocol": "HTTP",
        }

    def setUp(self) -> None:
        self.server_type_enricher.server_type_dict = {"dns": set(), "dhcp": set()}

    def test_header(self) -> None:
        expected_header = "is_dhcp,is_dns"
        self.assertEqual(self.server_type_enricher.header, expected_header)

    def test_detect_type_dhcp(self) -> None:
        expected_value = "True"
        actual_value = self.server_type_enricher.detect_type(self.dhcp_packet, ResponseHelper.is_dhcp_response, "dhcp")
        self.assertEqual(actual_value, expected_value)
        actual_value = self.server_type_enricher.detect_type(self.dns_packet, ResponseHelper.is_dhcp_response, "dhcp")
        self.assertNotEqual(actual_value, expected_value)

    def test_detect_type_dnd(self) -> None:
        expected_value = "True"
        actual_value = self.server_type_enricher.detect_type(self.dhcp_packet, ResponseHelper.is_dhcp_response, "dns")
        self.assertEqual(actual_value, expected_value)
        actual_value = self.server_type_enricher.detect_type(self.dns_packet, ResponseHelper.is_dhcp_response, "dns")
        self.assertNotEqual(actual_value, expected_value)

    def test_save_entry_dhcp(self) -> None:
        set_size = 0
        key = "dhcp"
        self.assertEqual(len(self.server_type_enricher.server_type_dict[key]), set_size)

        self.server_type_enricher.save_entry(key, self.dhcp_packet)
        set_size += 1
        self.assertEqual(len(self.server_type_enricher.server_type_dict[key]), set_size)
        self.server_type_enricher.save_entry(key, self.dhcp_packet)
        self.assertEqual(len(self.server_type_enricher.server_type_dict[key]), set_size)

    def test_save_entry_dns(self) -> None:
        set_size = 0
        key = "dns"
        self.assertEqual(len(self.server_type_enricher.server_type_dict[key]), set_size)

        self.server_type_enricher.save_entry(key, self.dhcp_packet)
        set_size += 1
        self.assertEqual(len(self.server_type_enricher.server_type_dict[key]), set_size)
        self.server_type_enricher.save_entry(key, self.dhcp_packet)
        self.assertEqual(len(self.server_type_enricher.server_type_dict[key]), set_size)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServerTypeEnricher)
    unittest.TextTestRunner(verbosity=2).run(suite)
