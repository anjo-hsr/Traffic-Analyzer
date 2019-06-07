import unittest
from unittest.mock import patch, MagicMock, mock_open

from main.helpers.dns_helper import DnsHelper


class TestDomainDictHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dns_helper = DnsHelper()

    def test_set_lifetime(self) -> None:
        default_dns_lifetime = 2
        self.assertTrue(self.dns_helper.dns_resolver.lifetime, default_dns_lifetime)
        self.assertTrue(self.dns_helper.dns_resolver_tester.lifetime, default_dns_lifetime)
        dns_lifetime = 1
        self.dns_helper.set_lifetime(dns_lifetime)
        self.assertTrue(self.dns_helper.dns_resolver.lifetime, dns_lifetime)
        self.assertTrue(self.dns_helper.dns_resolver_tester.lifetime, dns_lifetime)

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data="[Stanza]\n" + "internal_dns_servers = 8.8.8.8"))
    def test_set_dns_server(self) -> None:
        expected_length = len(self.dns_helper.dns_resolver.nameservers) + 1
        self.dns_helper.set_dns_server()
        self.assertEqual(len(self.dns_helper.dns_resolver.nameservers), expected_length)

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data="[Stanza]\n" + "internal_dns_servers = 1.1.1.1, 8.8.8.8"))
    def test_set_dns_servers(self) -> None:
        expected_length = len(self.dns_helper.dns_resolver.nameservers) + 2
        self.dns_helper.set_dns_server()
        self.assertEqual(len(self.dns_helper.dns_resolver.nameservers), expected_length)

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data="[Stanza]\n" + "internal_dns_servers = 8.8.8.8"))
    def test_reset_dns_server(self) -> None:
        expected_length = len(self.dns_helper.dns_resolver.nameservers) + 1
        self.dns_helper.set_dns_server()
        self.assertEqual(len(self.dns_helper.dns_resolver.nameservers), expected_length)
        expected_length -= 1
        self.dns_helper.reset_dns_resolver()
        self.assertEqual(len(self.dns_helper.dns_resolver.nameservers), expected_length)

    def test_is_dns_server_available_ok(self) -> None:
        dns_server_address = "8.8.8.8"
        self.assertTrue(self.dns_helper.is_dns_server_available(dns_server_address))

    def test_is_dns_server_avaiable_not_ok(self) -> None:
        dns_server_address = "127.0.0.1"
        self.assertFalse(self.dns_helper.is_dns_server_available(dns_server_address))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDomainDictHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
