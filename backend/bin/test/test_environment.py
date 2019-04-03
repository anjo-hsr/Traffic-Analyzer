import unittest

from os import path

from main.helpers.Environment import Environment


class TestCombinerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.environment_variables = {
            "pcap_path": path.join("..", "..", "..", "docker", "init_files", "pcaps"),
            "csv_path": path.join("..", "files")
        }

    def test_environment_test(self):
        self.assertEqual(Environment.get_environment(), self.environment_variables)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCombinerMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
