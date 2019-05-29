import unittest

from main.helpers.response_helper import ResponseHelper


class TestResponseHelper(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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

    def test_is_dhcp_response(self) -> None:
        self.assertTrue(ResponseHelper.is_dhcp_response(self.dhcp_packet))
        self.assertFalse(ResponseHelper.is_dhcp_response(self.dns_packet))
        self.assertFalse(ResponseHelper.is_dhcp_response(self.normal_packet))

    def test_is_dns_response(self) -> None:
        self.assertFalse(ResponseHelper.is_dns_response(self.dhcp_packet))
        self.assertTrue(ResponseHelper.is_dns_response(self.dns_packet))
        self.assertFalse(ResponseHelper.is_dns_response(self.normal_packet))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestResponseHelper)
    unittest.TextTestRunner(verbosity=2).run(suite)
