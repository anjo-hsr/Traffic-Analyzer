import unittest

from main.downloaders.ip_information_downloader import IpInformationDownloader


class TestIpInformationDownloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_ip = "10.0.0.1"
        cls.public_ip = "8.8.8.8"
        cls.empty_ip_data = {
            "rdns": cls.private_ip,
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

    def test_get_ip_information_private(self):
        ip_address = self.private_ip
        self.assertDictEqual(self.ip_information_downloader.get_ip_information(ip_address), self.empty_ip_data)

    def test_get_ip_data(self):
        ip_address = self.public_ip
        self.assertDictEqual(IpInformationDownloader.get_ip_data(ip_address), self.google_ip_data)

    def test_get_ip_information_twice(self):
        ip_address = self.private_ip
        length = 1
        self.assertEqual(self.ip_information_downloader.get_ip_information(ip_address), self.empty_ip_data)
        self.assertEqual(len(self.ip_information_downloader.ip_information), length)

        self.assertEqual(self.ip_information_downloader.get_ip_information(ip_address), self.empty_ip_data)
        self.assertEqual(len(self.ip_information_downloader.ip_information), length)

    def test_get_empty_ip_data(self):
        ip_address = self.private_ip
        self.assertEqual(IpInformationDownloader.get_empty_ip_data(ip_address), self.empty_ip_data)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIpInformationDownloader)
    unittest.TextTestRunner(verbosity=2).run(suite)
