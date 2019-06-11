import unittest
from os import path
from unittest.mock import patch

from main.helpers.environment_helper import EnvironmentHelper


class Process:
    def __init__(self, name) -> None:
        self.info = {"name": name}


class TestEnrivonmentHelperMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.environment_helper = EnvironmentHelper()
        cls.traffic_analyzer_base_path = path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer")
        cls.local_base_path = path.join(cls.traffic_analyzer_base_path, "local")
        cls.lookup_base_path = path.join(cls.traffic_analyzer_base_path, "lookups")
        cls.tmp_base_path = path.join("/tmp")
        cls.file_path = path.join("..", "files")

        cls.development_variables = {
            "environment": "development",
            "csv_tmp_path": cls.file_path,
            "csv_list_path": cls.file_path,
            "csv_capture_path": cls.file_path,
            "dns_request_files": cls.file_path,
            "configuration_folder": path.join("..", "..", "..", "frontend", "local")
        }
        cls.production_variables = {
            "environment": "production",
            "csv_tmp_path": path.join(cls.traffic_analyzer_base_path, "bin", "files"),
            "csv_list_path": path.join(cls.lookup_base_path, "lists"),
            "csv_capture_path": path.join(cls.lookup_base_path, "captures"),
            "dns_request_files": path.join(cls.lookup_base_path, "dns_request_files"),
            "configuration_folder": path.join(cls.local_base_path)
        }

    @patch("psutil.process_iter")
    def test_development_variables(self, process_iter) -> None:
        process = Process("dev_test")
        process_iter.return_value = [process]
        self.assertEqual(self.environment_helper.get_environment(), self.development_variables)

    @patch("psutil.process_iter")
    def test_production_variables(self, process_iter) -> None:
        process = Process("splunkd")
        process_iter.return_value = [process]
        self.assertEqual(self.environment_helper.get_environment(), self.production_variables)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnrivonmentHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
