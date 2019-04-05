import unittest

import main.downloaders.get_ciphers as get_ciphers


class TestGetCiphersMethods(unittest.TestCase):
    def test_calculate_hex(self):
        hex_dict = {
            "0x00,0x20": 32,
            "0xc0,0x28": 49192
        }
        for hex_line in hex_dict:
            self.assertEqual(get_ciphers.calculate_hex(hex_line), hex_dict[hex_line])

    def test_combine_information(self):
        row_dict = {
            "Value": "0xC0, 0x30",
            "Description": "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "Recommended": "Y",
        }
        expected_line = "49200,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,Y"

        actual_line = get_ciphers.combine_information(row_dict)
        self.assertEqual(actual_line, expected_line)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGetCiphersMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
