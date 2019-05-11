import unittest
from os import path, remove

import main.downloaders.mac_vendor_downloader as get_mac


class TestMacVendorDownloaderMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.row_dict = {
            "Assignment": "3CD92B",
            "Organization Name": "Hewlett Packard"
        }
        cls.vendor_mac = "3c:d9:2b"
        cls.expected_line = '3c:d9:2b,"Hewlett Packard"'

    def test_convert_to_vendor_mac(self) -> None:
        self.assertEqual(get_mac.convert_mac_address(self.row_dict), self.vendor_mac)

    def test_write_row_successful(self) -> None:
        test_file_path = path.join(".", "test.csv")
        with open(test_file_path, mode="w") as test_file:
            get_mac.write_row(test_file, self.row_dict)

        with open(test_file_path) as test_file:
            self.assertEqual(test_file.read(), self.expected_line + "\n")

        remove(test_file_path)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMacVendorDownloaderMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
