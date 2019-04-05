import unittest

import main.downloaders.get_mac as get_mac


class TestGetMacMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.line = {
            "Assignment": "FFFFFF",
            "Organization Name": "Broadcast Corp"
        }
        cls.vendor_mac = "ff:ff:ff"

    def test_convert_to_vendor_mac(self):
        self.assertEqual(get_mac.convert_mac_address(self.line), self.vendor_mac)

    def test_write_row(self):
        line_counter = 0
        self.assertEqual(get_mac.write_row(line_counter, None, {}), line_counter + 1)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGetMacMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
