import unittest
from unittest.mock import patch, mock_open, MagicMock

from main.helpers.file import file_read_helper


class TestFileReadHelperMethods(unittest.TestCase):
    def test_get_dict_reader(self) -> None:
        header1, header2 = "mac.vendor.part", "vendor"
        value1, value2 = "3c:d9:2b", "Hewlett Packard"

        csv_file = '{},{}\n{},"{}"'.format(header1, header2, value1, value2).splitlines()
        dict_reader = file_read_helper.get_csv_dict_reader(csv_file)

        field_names = [header1, header2]
        self.assertEqual(dict_reader.fieldnames, field_names)

        for row in dict_reader:
            self.assertEqual(row[header1], value1)
            self.assertEqual(row[header2], value2)

    def test_is_header(self) -> None:
        line_dict = {
            0: True,
            1: False
        }
        for key in line_dict:
            self.assertEqual(file_read_helper.is_header(key), line_dict[key])

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data="[Stanza]\n" + "test_key=test_value\n" + "hsr = rapperswil"))
    def test_get_config_value(self) -> None:
        file_path = "test_path"
        search_key = "test_key"
        expected_value = "test_value"
        self.assertEqual(file_read_helper.get_config_value(file_path, search_key), expected_value)

        search_key = "hsr"
        expected_value = "rapperswil"
        self.assertEqual(file_read_helper.get_config_value(file_path, search_key), expected_value)

    @patch("os.path.isfile", MagicMock(return_value=True))
    @patch("main.helpers.file.file_read_helper.open",
           new=mock_open(read_data=b"[Stanza]\n" + b"test_key=test_value\n" + b"hsr = rapperswil"))
    def test_get_file_hashsum(self) -> None:
        file_path = "test_path"
        expected_hash = "73ab4e71d2aca11a7fd9f7294692f090e804eb7e4093bb3035879cf216d49a6c"
        self.assertEqual(file_read_helper.get_file_hashsum(file_path), expected_hash)

    @patch("os.path.isfile", MagicMock(return_value=False))
    def test_get_file_hashsum_file_not_found(self) -> None:
        file_path = ""
        expected_hash = ""
        self.assertEqual(file_read_helper.get_file_hashsum(file_path), expected_hash)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileReadHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
