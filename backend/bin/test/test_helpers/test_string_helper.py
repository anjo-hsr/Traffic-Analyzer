import unittest

from main.helpers.string_helper import remove_quotations, enclose_with_quotes


class TestStringHelperMethods(unittest.TestCase):

    def test_remove_quotations(self) -> None:
        string_with_quotations = '"hsr","rapperswil","st. gallen","switzerland"'
        expected_string = "hsr,rapperswil,st. gallen,switzerland"
        self.assertEqual(remove_quotations(string_with_quotations), expected_string)

    def test_enclude_with_quotes(self) -> None:
        string_value = "hsr"
        expected_string = '"hsr"'
        self.assertEqual(enclose_with_quotes(string_value), expected_string)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
