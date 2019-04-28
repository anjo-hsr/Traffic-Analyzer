import unittest
from unittest.mock import patch, MagicMock

from main.downloaders.ip_information_downloader import IpInformationDownloader
from main.helpers.ip_helper import IpHelper


class TestIpInformationDownloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_ip = "10.0.0.1"
        cls.multicast_ip = "224.0.0.1"
        cls.public_ip = "8.8.8.8"
        cls.ip_data_private = {
            "rdns": "router.hsr.ch",
            "asn": "",
            "isp": "",
            "latitude": "",
            "longitude": ""
        }

        cls.ip_data_multicast = {
            "rdns": cls.multicast_ip,
            "asn": "",
            "isp": "",
            "latitude": "",
            "longitude": ""
        }

        cls.google_ip_data = {
            'rdns': 'google-public-dns-a.google.com',
            'asn': 15169,
            'isp': 'Google LLC',
            'latitude': 37.751,
            'longitude': -97.822,
        }

    def setUp(self):
        self.ip_information_downloader = IpInformationDownloader()

    @patch("socket.getfqdn", MagicMock(return_value="router.hsr.ch"))
    def test_get_ip_information_private(self):
        ip_address = self.private_ip
        self.ip_information_downloader.get_ip_information(ip_address)
        self.assertEqual(self.ip_information_downloader.ip_information[ip_address], self.ip_data_private)

    def test_get_ip_data(self):
        ip_address = self.public_ip
        self.assertDictEqual(IpInformationDownloader.get_ip_data(ip_address), self.google_ip_data)

    @patch("socket.getfqdn", MagicMock(return_value="router.hsr.ch"))
    def test_get_ip_information_twice(self):
        ip_address = self.private_ip
        length = 1
        self.ip_information_downloader.get_ip_information(ip_address)
        self.assertEqual(self.ip_information_downloader.ip_information[ip_address], self.ip_data_private)
        self.assertEqual(len(self.ip_information_downloader.ip_information), length)

        self.ip_information_downloader.get_ip_information(ip_address)
        self.assertEqual(self.ip_information_downloader.ip_information[ip_address], self.ip_data_private)
        self.assertEqual(len(self.ip_information_downloader.ip_information), length)

    def test_get_private_ip_data_multicast(self):
        ip_address = self.multicast_ip
        ip_helper = IpHelper()
        self.assertEqual(IpInformationDownloader.get_private_ip_data(ip_address, ip_helper), self.ip_data_multicast)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIpInformationDownloader)
    unittest.TextTestRunner(verbosity=2).run(suite)
