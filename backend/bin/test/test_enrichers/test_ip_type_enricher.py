import unittest

from main.enrichers.ip_type_enricher import IpTypeEnricher


class TestLocationEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ip_type_enricher = IpTypeEnricher()
        cls.private_ip = "10.0.0.1"
        cls.public_ip = "8.8.8.8"
        cls.multicast_ip = "224.0.0.1"

    def test_header(self) -> None:
        expected_header = "dst_is_private_ip,src_is_private_ip"
        self.assertEqual(self.ip_type_enricher.header, expected_header)

    def test_is_private(self) -> None:
        false_string = str(False)
        true_string = str(True)
        self.assertEqual(self.ip_type_enricher.is_private(self.private_ip), true_string)
        self.assertEqual(self.ip_type_enricher.is_private(self.public_ip), false_string)
        self.assertEqual(self.ip_type_enricher.is_private(self.multicast_ip), false_string)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocationEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
