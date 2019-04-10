import unittest

from os import path, remove

import main.downloaders.cipher_downloader as get_ciphers


class TestCipherDownloaderMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row_dict = {
            "Value": "0xC0, 0x30",
            "Description": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "Recommended": "Y",
        }
        cls.expected_line = "49200,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,Y"

    def test_calculate_hex(self):
        hex_dict = {
            "0x00,0x20": 32,
            "0xc0,0x28": 49192
        }
        for hex_line in hex_dict:
            self.assertEqual(get_ciphers.calculate_hex(hex_line), hex_dict[hex_line])

    def test_combine_information(self):
        actual_line = get_ciphers.combine_information(self.row_dict)
        self.assertEqual(actual_line, self.expected_line)

    def test_write_row_successful(self):
        test_file_path = path.join(".", "test.csv")
        with open(test_file_path, mode="w") as test_file:
            get_ciphers.write_row(test_file, self.row_dict)

        with open(test_file_path) as test_file:
            self.assertEqual(test_file.read(), self.expected_line + "\n")

        remove(test_file_path)

    def test_write_row_failing(self):
        test_file_path = path.join(".", "test.csv")
        row_dict = self.row_dict.copy()
        row_dict["Value"] = "0xC0, 0x2F-30"
        with open(test_file_path, mode="w") as test_file:
            get_ciphers.write_row(test_file, row_dict)

        with open(test_file_path) as test_file:
            self.assertEqual(test_file.read(), "")

        remove(test_file_path)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCipherDownloaderMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
