import unittest

from main.helpers.ip_helper import IpHelper


class TestIpHelperMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ip_helper = IpHelper()

    def test_public_ip_everything(self):
        everything_ip = "0.0.0.0"
        self.assertFalse(self.ip_helper.is_global_ip(everything_ip))

    def test_public_ip_private_ip(self):
        private_ips = ["10.0.0.1", "172.16.0.1", "192.168.0.1"]
        for private_ip in private_ips:
            self.assertFalse(self.ip_helper.is_global_ip(private_ip))

    def test_public_ip_public_ip(self):
        public_ips = ["8.8.8.8", "177.77.77.77", "199.99.99.99"]
        for public_ip in public_ips:
            self.assertTrue(self.ip_helper.is_global_ip(public_ip))

    def test_public_ip_multicast_ip(self):
        public_ips = ["224.0.0.0", "239.255.255.255"]
        for public_ip in public_ips:
            self.assertFalse(self.ip_helper.is_global_ip(public_ip))

    def test_public_ip_reserved_ip(self):
        reserved_ips = ["240.0.0.0", "255.255.255.254"]
        for reserved_ip in reserved_ips:
            self.assertFalse(self.ip_helper.is_global_ip(reserved_ip))

    def test_public_ip_error(self):
        wrong_ips = ["8.8.8.8.8", "127.0.1", '"localhost"']
        for wrong_ip in wrong_ips:
            self.assertFalse(self.ip_helper.is_global_ip(wrong_ip))

    def test_is_ip_good(self):
        correct_ips = ["8.8.8.8", "127.0.0.1"]
        for correct_ip in correct_ips:
            self.assertTrue(self.ip_helper.is_ip(correct_ip))

    def test_is_ip_error(self):
        wrong_ips = ["8.8.8.8.8", "127.0.1", '"localhost"']
        for wrong_ip in wrong_ips:
            self.assertFalse(self.ip_helper.is_ip(wrong_ip))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIpHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
