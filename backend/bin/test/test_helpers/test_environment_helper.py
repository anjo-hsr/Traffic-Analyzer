import unittest

from os import path
from unittest.mock import patch

from main.helpers.environment_helper import EnvironmentHelper


class Process():
    def __init__(self, name):
        self.info = {"name": name}


class TestEnrivonmentHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.environment_helper = EnvironmentHelper()

        cls.development_variables = {
            "pcap_path": path.join("..", "..", "..", "docker", "init_files", "pcaps"),
            "pcap_processed_path": path.join("..", "..", "..", "docker", "init_files", "pcaps"),
            "csv_tmp_path": path.join("..", "files"),
            "csv_list_path": path.join("..", "files"),
            "csv_capture_path": path.join("..", "files")
        }
        cls.production_variables = {
            "pcap_path": path.join("/tmp", "pcaps"),
            "pcap_processed_path": path.join("/tmp", "pcaps_processed"),
            "csv_tmp_path": path.join("/tmp", "csvs"),
            "csv_list_path": path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer", "lookups", "lists"),
            "csv_capture_path": path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer", "lookups", "captures")
        }

    @patch("psutil.process_iter")
    def test_development_variables(self, process_iter):
        process = Process("dev_test")
        process_iter.return_value = [process]
        self.assertEqual(self.environment_helper.get_environment(), self.development_variables)

    @patch("psutil.process_iter")
    def test_production_variables(self, process_iter):
        process = Process("splunkd")
        process_iter.return_value = [process]
        self.assertEqual(self.environment_helper.get_environment(), self.production_variables)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrivonmentHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
