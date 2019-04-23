import unittest
from io import StringIO
from unittest.mock import patch

from main.helpers.print_helper import PrintHelper


class TestPrintHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = ["Rapperswil", "Zurich"]
        cls.cantons = {"Rapperswil": "St. Gallen", "Zurich": "Zurich"}

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_dict(self, mock_stdout):
        text_with_placeholders = "Print out for all {} cities"
        PrintHelper.print_list(self.cities, text_with_placeholders)

        print_text = "Print out for all {} cities\n" \
                     "Rapperswil, Zurich\n\n\n\n".format(len(self.cities))
        self.assertEqual(mock_stdout.getvalue(), print_text)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_list(self, mock_stdout):
        text_with_placeholders = "Print out for all {} cities to canton entries"
        PrintHelper.print_dict(self.cantons, text_with_placeholders)

        print_text = "Print out for all {} cities to canton entries\n" \
                     "Rapperswil --> St. Gallen\n" \
                     "Zurich --> Zurich\n\n\n\n".format(len(self.cantons))
        self.assertEqual(mock_stdout.getvalue(), print_text)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_error(self, mock_stdout):
        error_text = "No wireshark folder found. Please install Wireshark into the standard folder"

        PrintHelper.print_error(error_text)

        banner = "#" * 120
        general_text = "An error occured:"
        print_elements = [banner, general_text, error_text, banner]
        print_text = "\n".join(element for element in print_elements) + "\n"
        self.assertEqual(mock_stdout.getvalue(), print_text)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPrintHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
