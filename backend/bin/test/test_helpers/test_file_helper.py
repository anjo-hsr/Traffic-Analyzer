import unittest

from os import path, remove

import main.helpers.file_helper as file_helper
from main.helpers.environment_helper import EnvironmentHelper

from test.filenames import Filenames


class TestFileHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filenames = Filenames.get_filenames()
        cls.csv_filenames = filenames["csv_filenames"]
        cls.csv_enriched_filenames = filenames["csv_enriched_filenames"]
        cls.pcap_filenames_without_prefix = filenames["pcap_filenames_without_prefix"]
        cls.pcapng_filenames_without_prefix = filenames["pcapng_filenames_without_prefix"]
        cls.pcap_filenames_with_prefix = filenames["pcap_filenames_with_prefix"]
        cls.pcapng_filenames_with_prefix = filenames["pcapng_filenames_with_prefix"]

    def test_get_dict_reader(self):
        header1, header2 = "mac.vendor.part", "vendor"
        value1, value2 = "3c:d9:2b", "Hewlett Packard"

        csv_file = '{},{}\n{},"{}"'.format(header1, header2, value1, value2).splitlines()
        dict_reader = file_helper.get_csv_dict_reader(csv_file)

        field_names = [header1, header2]
        self.assertEqual(dict_reader.fieldnames, field_names)

        for row in dict_reader:
            self.assertEqual(row[header1], value1)
            self.assertEqual(row[header2], value2)

    def test_download_and_remove(self):
        environment_helper = EnvironmentHelper()
        environment_variables = environment_helper.get_environment()
        filename = path.join(environment_variables["csv_tmp_path"], "README.md")
        self.assertFalse(path.isfile(filename))

        url = "https://raw.githubusercontent.com/anjo-hsr/Traffic-Analyzer/master/README.md"
        downloaded_filename = file_helper.download_file(url)
        self.assertTrue(downloaded_filename, filename)
        self.assertTrue(path.isfile(filename))

        file_helper.remove_file(filename)
        self.assertFalse(path.isfile(filename))

    def test_is_header(self):
        line_dict = {
            0: True,
            1: False
        }
        for key in line_dict:
            self.assertEqual(file_helper.is_header(key), line_dict[key])

    def test_write_line(self):
        line = "test123"
        test_file_path = path.join(".", "test.csv")
        with open(test_file_path, mode="w") as test_file:
            file_helper.write_line(test_file, line)

        with open(test_file_path) as test_file:
            self.assertEqual(test_file.read(), line + "\n")

        remove(test_file_path)

    def test_move_file(self):
        source_path = path.join(".", ".test_file")
        destination_path = path.join(".", ".test_file-moved")
        open(source_path, 'a').close()

        self.assertNotEqual(path.isfile(source_path), path.isfile(destination_path))
        file_helper.move_file(source_path, destination_path)
        self.assertNotEqual(path.isfile(source_path), path.isfile(destination_path))
        file_helper.move_file(destination_path, source_path)
        self.assertNotEqual(path.isfile(source_path), path.isfile(destination_path))

        file_helper.remove(source_path)
        self.assertFalse(path.isfile(source_path))
        self.assertFalse(path.isfile(destination_path))

    def test_pcap_pcapng_filenames(self):
        for filename in self.pcap_filenames_with_prefix:
            self.assertTrue(file_helper.is_pcap_file(filename))

        for filename in self.pcapng_filenames_with_prefix:
            self.assertTrue(file_helper.is_pcap_file(filename))

        for filename in self.csv_filenames:
            self.assertFalse(file_helper.is_pcap_file(filename))

    def test_is_normal_csv(self):
        for filename in self.csv_filenames:
            self.assertTrue(file_helper.is_normal_csv_file(filename))

        for filename in self.csv_enriched_filenames:
            self.assertFalse(file_helper.is_normal_csv_file(filename))

    def test_is_enriched_csv(self):
        for filename in self.csv_enriched_filenames:
            self.assertTrue(file_helper.is_enriched_csv_file(filename))

        for filename in self.csv_filenames:
            self.assertFalse(file_helper.is_enriched_csv_file(filename))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
