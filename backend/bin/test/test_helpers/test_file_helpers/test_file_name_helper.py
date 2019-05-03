import unittest

from main.helpers.file import file_name_helper
from test.filenames import get_filenames


class TestFileNameHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filenames = get_filenames()
        cls.csv_filenames = filenames["csv_filenames"]
        cls.csv_enriched_filenames = filenames["csv_enriched_filenames"]
        cls.pcap_filenames_without_prefix = filenames["pcap_filenames_without_prefix"]
        cls.pcapng_filenames_without_prefix = filenames["pcapng_filenames_without_prefix"]
        cls.pcap_filenames_with_prefix = filenames["pcap_filenames_with_prefix"]
        cls.pcapng_filenames_with_prefix = filenames["pcapng_filenames_with_prefix"]

    def test_pcap_pcapng_filenames(self):
        for filename in self.pcap_filenames_with_prefix:
            self.assertTrue(file_name_helper.is_pcap_file(filename))

        for filename in self.pcapng_filenames_with_prefix:
            self.assertTrue(file_name_helper.is_pcap_file(filename))

        for filename in self.csv_filenames:
            self.assertFalse(file_name_helper.is_pcap_file(filename))

    def test_is_normal_csv(self):
        for filename in self.csv_filenames:
            self.assertTrue(file_name_helper.is_normal_csv_file(filename))

        for filename in self.csv_enriched_filenames:
            self.assertFalse(file_name_helper.is_normal_csv_file(filename))

    def test_is_enriched_csv(self):
        for filename in self.csv_enriched_filenames:
            self.assertTrue(file_name_helper.is_enriched_csv_file(filename))

        for filename in self.csv_filenames:
            self.assertFalse(file_name_helper.is_enriched_csv_file(filename))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileNameHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
