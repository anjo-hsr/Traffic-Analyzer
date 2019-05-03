import unittest
from unittest.mock import patch, MagicMock

from main.helpers.file import file_path_helper, file_name_helper


class TestFilePathHelperMethods(unittest.TestCase):
    @patch(
        "main.helpers.file.file_path_helper.walk",
        MagicMock(return_value=[
            ("/tmp/pcaps", [], ["test1.pcap", "test2.pcapng"])
        ])
    )
    def test_get_file_paths_pcap(self):
        expected_file_paths = [{"filename": "test1.pcap", "path": "/tmp/pcaps"},
                               {"filename": "test2.pcapng", "path": "/tmp/pcaps"}]
        file_paths = file_path_helper.get_file_paths("", file_name_helper.is_pcap_file)
        self.assertEqual(file_paths, expected_file_paths)

    @patch(
        "main.helpers.file.file_path_helper.walk",
        MagicMock(return_value=[
            ("/tmp/csvs", [], ["capture-test1.csv", "capture-test2.csv"])
        ])
    )
    def test_get_file_paths_csv(self):
        expected_file_paths = [{"filename": "capture-test1.csv", "path": "/tmp/csvs"},
                               {"filename": "capture-test2.csv", "path": "/tmp/csvs"}]
        file_paths = file_path_helper.get_file_paths("", file_name_helper.is_normal_csv_file)
        self.assertEqual(file_paths, expected_file_paths)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFilePathHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
