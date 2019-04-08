import unittest

from os import path
from unittest.mock import patch, MagicMock

from main.helpers.Environment import Environment


class TestEnvironmentMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.development_variables = {
            "pcap_path": path.join("..", "..", "..", "docker", "init_files", "pcaps"),
            "csv_path": path.join("..", "files"),
            "csv_enriched_path": path.join("..", "files")
        }

        cls.production_variables = {
            "pcap_path": path.join("/tmp", "pcaps"),
            "csv_path": path.join("/tmp", "csvs"),
            "csv_enriched_path": path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer", "lookups")
        }

    @patch.dict("os.environ", {})
    def test_development_variables(self):
        self.assertEqual(Environment.get_environment(), self.development_variables)

    @patch.dict("os.environ", {"SPLUNK_HOME": "/opt/splunk"})
    def test_production_variables(self):
        self.assertEqual(Environment.get_environment(), self.production_variables)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnvironmentMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
