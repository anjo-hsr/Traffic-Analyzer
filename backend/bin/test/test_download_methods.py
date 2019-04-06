import unittest

from os import path, remove

import main.downloaders.download_methods as download_methods


class TestGetMacMethods(unittest.TestCase):
    def test_download_and_remove(self):
        filename = "README.md"
        self.assertFalse(path.isfile(filename))

        url = "https://raw.githubusercontent.com/anjo-hsr/Traffic-Analyzer/master/README.md"
        downloaded_filename = download_methods.download_file(url)
        self.assertTrue(downloaded_filename, filename)
        self.assertTrue(path.isfile(filename))

        download_methods.remove_downloaded_file(filename)
        self.assertFalse(path.isfile(filename))

    def test_is_header(self):
        line_dict = {
            0: True,
            1: False
        }
        for key in line_dict:
            self.assertEqual(download_methods.is_header(key), line_dict[key])

    def test_write_line(self):
        line = "test123"
        test_file_path = path.join(".", "test.csv")
        with open(test_file_path, mode="w") as test_file:
            download_methods.write_line(test_file, line)

        with open(test_file_path) as test_file:
            self.assertEqual(test_file.read(), line + "\n")

        remove(test_file_path)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGetMacMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
