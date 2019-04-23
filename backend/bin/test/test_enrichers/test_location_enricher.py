import unittest

from main.enrichers.location_enricher import LocationEnricher


class TestLocationEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.public_ip_address = "152.96.36.100"
        cls.private_ip_address = "10.0.0.1"
        cls.dst_src = {"dst": cls.public_ip_address, "src": cls.private_ip_address}
        cls.location = [47.1449, 8.1551]
        cls.empty_location = ["", ""]

    def setUp(self):
        self.location_enricher = LocationEnricher()

    def assert_location(self, ip_address, location):
        self.location_enricher.get_location(ip_address)
        self.assertEqual(self.location_enricher.locations[ip_address], location)

    def test_get_location(self):
        lat_long = self.location_enricher.locate_ip(self.public_ip_address)
        self.assertEqual(lat_long, self.location)

    def test_locate_public_ip_first_time(self):
        ip_address = self.public_ip_address
        self.assert_location(ip_address, self.location)

        size_before = len(self.location_enricher.locations)
        self.assert_location(ip_address, self.location)
        size_after = len(self.location_enricher.locations)
        self.assertEqual(size_after, size_before)

    def test_locate_private_ip(self):
        ip_address = self.private_ip_address
        self.assert_location(ip_address, self.empty_location)

    def test_locate_no_ip(self):
        ip_address = ""
        self.assert_location(ip_address, self.empty_location)

    def test_locate(self):
        line = self.location_enricher.locate(self.dst_src)
        expected_line = '"47.1449","8.1551","",""'
        self.assertEqual(line, expected_line)

    def tearDown(self):
        self.location_enricher = None


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocationEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
