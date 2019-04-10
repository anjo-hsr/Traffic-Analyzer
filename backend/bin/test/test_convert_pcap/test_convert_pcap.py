from io import StringIO

import unittest

from unittest.mock import patch

import main.convert_pcap as convert_pcap
from test.filenames import Filenames


class TestConvertPcapMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        filenames = Filenames.get_filenames()
        cls.csv_filenames = filenames["csv_filenames"]
        cls.pcap_filenames_without_prefix = filenames["pcap_filenames_without_prefix"]
        cls.pcapng_filenames_without_prefix = filenames["pcapng_filenames_without_prefix"]
        cls.pcap_filenames_with_prefix = filenames["pcap_filenames_with_prefix"]
        cls.pcapng_filenames_with_prefix = filenames["pcapng_filenames_with_prefix"]

    def test_get_new_filename_without_prefix(self):
        new_pcap_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcap_filenames_without_prefix
        ]
        new_pcapng_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcapng_filenames_without_prefix
        ]
        csv_filenames_lower = [filename.lower() for filename in self.csv_filenames]

        self.assertEqual(new_pcap_filenames, csv_filenames_lower)
        self.assertEqual(new_pcapng_filenames, csv_filenames_lower)

    def test_get_new_filename_with_prefix(self):
        new_pcap_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcap_filenames_with_prefix
        ]
        new_pcapng_filenames = [
            convert_pcap.get_new_filename(filename) for filename in self.pcapng_filenames_with_prefix
        ]
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
