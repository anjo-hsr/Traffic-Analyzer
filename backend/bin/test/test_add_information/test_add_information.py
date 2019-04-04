import unittest

import main.add_information as add_information
from main.helpers.Locator import Locator
from main.helpers.NameResolver import NameResolver
from main.helpers.CipherSuites import CipherSuites


class TestAddInformation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_create_helpers_classes(self):
        helpers = add_information.create_helpers()
        keys = helpers.keys()

        for key in keys:
            if key == "locator":
                self.assertTrue(isinstance(helpers[key], Locator))

            elif key == "name_resolver":
                self.assertTrue(isinstance(helpers[key], NameResolver))

            elif key == "cipher_suites":
                self.assertTrue(isinstance(helpers[key], CipherSuites))

            else:
                self.assertTrue(False)

    def test_create_helpers_is_dict(self):
        helpers = add_information.create_helpers()
        self.assertTrue(isinstance(helpers, dict))

    def test_create_helpers_keys(self):
        test_keys = ["locator", "name_resolver", "cipher_suites"]

        helpers = add_information.create_helpers()
        keys = [helper_key for helper_key in helpers]
        self.assertListEqual(keys, test_keys)

    def test_is_header(self):
        self.assertTrue(add_information.is_header(0))
        self.assertFalse(add_information.is_header(1))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddInformation)
    unittest.TextTestRunner(verbosity=2).run(suite)
