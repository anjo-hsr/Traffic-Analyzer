import unittest
from os import path
from unittest.mock import patch, MagicMock

from main.helpers.download_helper import DownloadHelper
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.file import file_move_helper


class TestFileMoveHelperMethods(unittest.TestCase):
    @patch(
        "main.helpers.environment_helper.EnvironmentHelper.get_environment",
        MagicMock(return_value={"csv_tmp_path": path.join(".")})
    )
    def test_download_and_remove(self) -> None:
        environment_helper = EnvironmentHelper()
        environment_variables = environment_helper.get_environment()

        filename = "README.md"
        file_path = path.join(environment_variables["csv_tmp_path"], filename)
        self.assertFalse(path.isfile(file_path))

        url = "https://raw.githubusercontent.com/anjo-hsr/Traffic-Analyzer/master/README.md"
        downloaded_filename = DownloadHelper.store_file(url)
        self.assertTrue(downloaded_filename, file_path)
        self.assertTrue(path.isfile(file_path))

        file_move_helper.remove_file(file_path)
        self.assertFalse(path.isfile(file_path))

    def test_move_file(self) -> None:
        source_path = path.join(".", "test_file")
        destination_path = path.join(".", "test_file-moved")

        open(source_path, 'a').close()
        self.assertTrue(path.isfile(source_path))
        self.assertNotEqual(path.isfile(source_path), path.isfile(destination_path))

        file_move_helper.move_file(source_path, destination_path)
        self.assertTrue(path.isfile(destination_path))
        self.assertNotEqual(path.isfile(source_path), path.isfile(destination_path))

        file_move_helper.remove(destination_path)
        self.assertFalse(path.isfile(source_path))
        self.assertFalse(path.isfile(destination_path))

    def test_move_file_same_path(self) -> None:
        source_path = path.join(".", ".test_file")
        destination_path = path.join(".", ".test_file")

        open(source_path, 'a').close()
        self.assertTrue(path.isfile(source_path))
        self.assertEqual(path.isfile(source_path), path.isfile(destination_path))

        file_move_helper.move_file(source_path, destination_path)
        self.assertTrue(path.isfile(destination_path))
        self.assertEqual(path.isfile(source_path), path.isfile(destination_path))

        file_move_helper.remove(source_path)
        self.assertFalse(path.isfile(source_path))
        self.assertFalse(path.isfile(destination_path))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileMoveHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
