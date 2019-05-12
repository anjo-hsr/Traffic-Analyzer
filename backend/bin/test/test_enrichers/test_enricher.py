import unittest
from io import StringIO
from unittest.mock import patch

from main.enrichers.enricher import Enricher


class TestDnsLookupEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_enricher_type = "test enricher"
        cls.test_header = ""
        cls.enricher = Enricher(cls.test_enricher_type, cls.test_header)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print(self, mock_stdout) -> None:
        print_text = "Nothing to print for {}.\n".format(self.test_enricher_type)
        self.enricher.print()
        self.assertEqual(mock_stdout.getvalue(), print_text)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDnsLookupEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
