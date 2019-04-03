import unittest

from os import path

from main.helpers.Environment import Environment


class TestCombinerMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.development_variables = {
            "pcap_path": path.join("/tmp", "pcaps"),
            "csv_path": path.join("/tmp", "csvs")
        }

        cls.production_variables = {
            "pcap_path": path.join("..", "..", "..", "docker", "init_files", "pcaps"),
            "csv_path": path.join("..", "files")
        }

    def test_development_variables(self):
        self.assertEqual(Environment.get_environment(), self.development_variables)

    def test_production_variables(self):
        self.assertEqual(Environment.get_environment(True), self.production_variables)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCombinerMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
