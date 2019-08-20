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
        cls.locally_administered_mac = "3e:d9:2b"

        cls.expected_universal_line = r'3c:d9:2b,"Hewlett Packard"'
        cls.expected_locally_line = r'3e:d9:2b,"Locally administered - Hewlett Packard"'

    def test_convert_to_vendor_mac(self) -> None:
        self.assertEqual(get_mac.convert_mac_address(self.row_dict), self.vendor_mac)

    def test_get_local_mac_address(self) -> None:
        self.assertEqual(get_mac.get_local_mac_address(self.vendor_mac), self.locally_administered_mac)

    def test_write_row_successful(self) -> None:
        test_file_path = path.join(".", "test.csv")
        with open(test_file_path, "w") as test_file:
            get_mac.write_row(test_file, self.row_dict)

        with open(test_file_path) as test_file:
            file_content = test_file.read()
            self.assertRegex(file_content, self.expected_universal_line)
            self.assertRegex(file_content, self.expected_locally_line)

        remove(test_file_path)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMacVendorDownloaderMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
