import unittest

from os import path

from main.helpers.Environment import Environment


class TestEnvironmentMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.development_variables = {
            "pcap_path": path.join("..", "..", "..", "docker", "init_files", "pcaps"),
            "csv_path": path.join("..", "files")
        }

        cls.production_variables = {
            "pcap_path": path.join("/tmp", "pcaps"),
            "csv_path": path.join("/tmp", "csvs")
        }

    @patch.dict("os.environ", {})
    def test_development_variables(self):
        self.assertEqual(Environment.get_environment(), self.development_variables)

    def test_production_variables(self):
        self.assertEqual(Environment.get_environment(True), self.production_variables)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnvironmentMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
