import unittest

from main.helpers import NameResolver


class TestNameResolverMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name_resolver = NameResolver()
        cls.source_ip_address = "10.0.0.1"
        cls.destination_ip_address = "152.96.36.100"
        cls.destination_fqdn = "lb-ext-web1.hsr.ch"

    def test_get_fqdn(self):
        self.name_resolver.get_fqdn(self.destination_ip_address)
        self.assertEqual(self.name_resolver.fqdns[self.destination_ip_address], self.destination_fqdn)

    def test_resolve(self):
        dst_src = {"dst": self.destination_ip_address, "src": self.source_ip_address}
        resolved_fqdns = '"{}","{}"'.format(self.destination_fqdn, self.source_ip_address)
        self.assertEqual(self.name_resolver.resolve(dst_src), resolved_fqdns)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNameResolverMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
