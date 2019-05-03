import unittest
from unittest.mock import patch, MagicMock

from main.downloaders.ip_information_downloader import IpInformationDownloader


class TestIpInformationDownloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_ip = "10.0.0.1"
        cls.multicast_ip = "224.0.0.1"
        cls.public_ip = "8.8.8.8"
        cls.ip_data_private = {
            "ip_address": cls.private_ip,
            "rdns": "router.hsr.ch",
            "asn": "",
            "isp": "",
            "latitude": "",
            "longitude": ""
        }

        cls.ip_data_multicast = {
            "ip_address": cls.multicast_ip,
            "rdns": cls.multicast_ip,
            "asn": "",
            "isp": "",
            "latitude": "",
            "longitude": ""
        }

        cls.ip_data_public = {
            "ip_address": cls.public_ip,
            'rdns': 'google-public-dns-a.google.com',
            'asn': 15169,
            'isp': 'Google LLC',
            'latitude': 37.751,
            'longitude': -97.822,
        }

    def setUp(self):
        self.ip_information_downloader = IpInformationDownloader()

    def assert_ip_data(self, ip_address, expected_ip_data):
        self.ip_information_downloader.get_ip_information(ip_address)
        ip_data = self.ip_information_downloader.ip_information[ip_address]
        self.assertEqual(ip_data, expected_ip_data)

    def test_get_ip_data_public(self):
        ip_address = self.public_ip
        self.assert_ip_data(ip_address, self.ip_data_public)

    @patch("socket.getfqdn", MagicMock(return_value="router.hsr.ch"))
    def test_get_ip_information_private(self):
        ip_address = self.private_ip
        self.assert_ip_data(ip_address, self.ip_data_private)

    def test_get_ip_data_multicast(self):
        ip_address = self.multicast_ip
        self.assert_ip_data(ip_address, self.ip_data_multicast)

    @patch("socket.getfqdn", MagicMock(return_value="router.hsr.ch"))
    def test_get_ip_information_twice(self):
        ip_address = self.private_ip
        length = 1
        self.assert_ip_data(ip_address, self.ip_data_private)
        self.assertEqual(len(self.ip_information_downloader.ip_information), length)

        self.assert_ip_data(ip_address, self.ip_data_private)
        self.assertEqual(len(self.ip_information_downloader.ip_information), length)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIpInformationDownloader)
    unittest.TextTestRunner(verbosity=2).run(suite)
