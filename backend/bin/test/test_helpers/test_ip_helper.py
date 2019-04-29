import unittest

from main.helpers.ip_helper import IpHelper


class TestIpHelperMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ip_helper = IpHelper()

    def test_everything_ip(self):
        everything_ip = "0.0.0.0"
        self.assertTrue(self.ip_helper.is_ip(everything_ip))
        self.assertFalse(self.ip_helper.is_global_ip(everything_ip))
        self.assertTrue(self.ip_helper.is_private_ip(everything_ip))
        self.assertFalse(self.ip_helper.is_multicast_ip(everything_ip))

    def test_public_ip(self):
        public_ips = ["8.8.8.8", "177.77.77.77", "199.99.99.99"]
        for public_ip in public_ips:
            self.assertTrue(self.ip_helper.is_ip(public_ip))
            self.assertTrue(self.ip_helper.is_global_ip(public_ip))
            self.assertFalse(self.ip_helper.is_private_ip(public_ip))
            self.assertFalse(self.ip_helper.is_multicast_ip(public_ip))

    def test_private_ip(self):
        private_ips = ["10.0.0.1", "172.16.0.1", "192.168.0.1"]
        for private_ip in private_ips:
            self.assertTrue(self.ip_helper.is_ip(private_ip))
            self.assertFalse(self.ip_helper.is_global_ip(private_ip))
            self.assertTrue(self.ip_helper.is_private_ip(private_ip))
            self.assertFalse(self.ip_helper.is_multicast_ip(private_ip))

    def test_multicast_ip(self):
        multicast_ips = ["224.0.0.0", "239.255.255.255"]
        for multicast_ip in multicast_ips:
            self.assertTrue(self.ip_helper.is_ip(multicast_ip))
            self.assertFalse(self.ip_helper.is_global_ip(multicast_ip))
            self.assertFalse(self.ip_helper.is_private_ip(multicast_ip))
            self.assertTrue(self.ip_helper.is_multicast_ip(multicast_ip))

    def test_reserved_ip(self):
        reserved_ips = ["240.0.0.0", "255.255.255.254"]
        for reserved_ip in reserved_ips:
            self.assertTrue(self.ip_helper.is_ip(reserved_ip))
            self.assertFalse(self.ip_helper.is_global_ip(reserved_ip))
            self.assertTrue(self.ip_helper.is_private_ip(reserved_ip))
            self.assertFalse(self.ip_helper.is_multicast_ip(reserved_ip))

    def test_fqdn_strings(self):
        fqdns = ["localhost", "www.hsr.ch"]
        for fqdn in fqdns:
            self.assertFalse(self.ip_helper.is_ip(fqdn))
            self.assertFalse(self.ip_helper.is_global_ip(fqdn))
            self.assertFalse(self.ip_helper.is_private_ip(fqdn))
            self.assertFalse(self.ip_helper.is_multicast_ip(fqdn))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIpHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
