import unittest

from main.helpers import string_helper


class TestStringHelperMethods(unittest.TestCase):

    def test_remove_quotations(self):
        string_with_quotations = '"hsr","rapperswil","st. gallen","switzerland"'
        expected_string = "hsr,rapperswil,st. gallen,switzerland"
        self.assertEqual(string_helper.remove_quotations(string_with_quotations), expected_string)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
