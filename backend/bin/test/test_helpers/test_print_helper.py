import unittest
from io import StringIO
from unittest.mock import patch

from main.enricher_jar import EnricherJar
from main.helpers.print_helper import PrintHelper


class TestPrintHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cities = ["Rapperswil", "Zurich"]
        cls.cantons = {"Rapperswil": "St. Gallen", "Zurich": "Zurich"}

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_dict(self, mock_stdout) -> None:
        text_with_placeholders = "Print out for all {} cities"
        PrintHelper.print_list(self.cities, text_with_placeholders)

        print_text = "Print out for all {} cities\n" \
                     "Rapperswil, Zurich\n\n\n\n".format(len(self.cities))
        self.assertEqual(mock_stdout.getvalue(), print_text)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_list(self, mock_stdout) -> None:
        text_with_placeholders = "Print out for all {} cities to canton entries"
        PrintHelper.print_dict(self.cantons, text_with_placeholders)

        print_text = "Print out for all {} cities to canton entries\n" \
                     "Rapperswil --> St. Gallen\n" \
                     "Zurich --> Zurich\n\n\n\n".format(len(self.cantons))
        self.assertEqual(mock_stdout.getvalue(), print_text)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_error(self, mock_stdout) -> None:
        error_text = "No wireshark folder found. Please install Wireshark into the standard folder"

        PrintHelper.print_error(error_text)

        banner = "#" * 120
        general_text = "An error occured:"
        print_elements = [banner, general_text, error_text, banner]
        print_text = "\n".join(element for element in print_elements) + "\n"
        self.assertEqual(mock_stdout.getvalue(), print_text)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_enrichers(self, mock_stdout) -> None:
        print_text = "Nothing to print for ip address combine enricher.\n" \
                     "Nothing to print for location enricher.\n" \
                     "Nothing to print for name resolve enricher.\n" \
                     "Print out for 1 tcp stream entries\n" \
                     " --> \n\n\n\n" \
                     "Print out for 0 streams to tls version entries\n\n\n\n" \
                     "Print out for all 0 streams to cipher suites entries\n\n\n\n" \
                     "Nothing to print for ip type enricher.\n" \
                     "Nothing to print for dns lookup enricher.\n" \
                     "Nothing to print for server type enricher.\n" \
                     "Nothing to print for ad enricher.\n" \
                     "Nothing to print for threat enricher.\n"

        enricher_jar = EnricherJar()
        PrintHelper.print_enrichers(enricher_jar.enricher_classes)
        self.assertEqual(mock_stdout.getvalue(), print_text)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_nothing(self, mock_stdout) -> None:
        enricher_type = "print helper tester"
        PrintHelper.print_nothing(enricher_type)
        print_text = "Nothing to print for print helper tester.\n"
        self.assertEqual(mock_stdout.getvalue(), print_text)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPrintHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
