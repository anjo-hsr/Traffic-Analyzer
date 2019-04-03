import unittest

import main.get_mac as get_mac


class TestGetMacMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mac_line = ["","FFFFFF"]
        cls.vendor_mac = "ff:ff:ff"

    def test_convert_to_vendor_mac(self):
        self.assertEqual(get_mac.convert_mac_address(self.mac_line), self.vendor_mac)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGetMacMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
