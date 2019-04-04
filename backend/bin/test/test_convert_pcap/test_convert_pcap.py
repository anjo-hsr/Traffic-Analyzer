from io import StringIO

import unittest

from unittest.mock import patch

import main.convert_pcap as convert_pcap
from test.file_names import FileNames


class TestConvertPcapMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filenames = FileNames.get_filenames()
        cls.csv_filenames = filenames["csv_filenames"]
        cls.pcap_filenames = filenames["pcap_filenames"]
        cls.pcapng_filenames = filenames["pcapng_filenames"]

    def test_csv_filenames(self):
        for filename in self.csv_filenames:
            self.assertTrue(convert_pcap.is_csv_file(filename))

        for filename in self.pcap_filenames:
            self.assertFalse(convert_pcap.is_csv_file(filename))

        for filename in self.pcapng_filenames:
            self.assertFalse(convert_pcap.is_csv_file(filename))

    def test_pcap_pcapng_filenames(self):
        for filename in self.pcap_filenames:
            self.assertTrue(convert_pcap.is_pcap_file(filename))

        for filename in self.pcapng_filenames:
            self.assertTrue(convert_pcap.is_pcap_file(filename))

        for filename in self.csv_filenames:
            self.assertFalse(convert_pcap.is_pcap_file(filename))

    def test_get_new_filename(self):
        new_pcap_filenames = [convert_pcap.get_new_filename(filename) for filename in self.pcap_filenames]
        new_pcapng_filenames = [convert_pcap.get_new_filename(filename) for filename in self.pcapng_filenames]
        csv_filenames_lower = [filename.lower() for filename in self.csv_filenames]

        self.assertEqual(new_pcap_filenames, csv_filenames_lower)
        self.assertEqual(new_pcapng_filenames, csv_filenames_lower)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_error(self, mock_stdout):
        error_text = "No wireshark folder found. Please install Wireshark into the standard folder\n"
        convert_pcap.print_error()
        self.assertEqual(mock_stdout.getvalue(), error_text)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvertPcapMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
