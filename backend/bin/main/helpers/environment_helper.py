from os import path
from typing import Dict

import psutil


class EnvironmentHelper:

    def __init__(self):
        self.production_process_name = "splunkd"

    def get_environment(self) -> Dict[str, str]:
        is_splunk_server = self.is_process_running(self.production_process_name)

        environment_variables = {}

        if is_splunk_server:
            splunk_app_folder = path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer")
            splunk_app_lookup_folder = path.join(splunk_app_folder, "lookups")

            environment_variables["csv_tmp_path"] = path.join(splunk_app_folder, "bin", "files")
            environment_variables["csv_capture_path"] = path.join(splunk_app_lookup_folder, "captures")
            environment_variables["csv_list_path"] = path.join(splunk_app_lookup_folder, "lists")
            environment_variables["dns_request_files"] = path.join(splunk_app_lookup_folder, "dns_request_files")
            environment_variables["configuration_folder"] = path.join(splunk_app_folder, "local")

        else:
            file_path = path.join("..", "files")
            frontend_folder = path.join("..", "..", "..", "frontend")

            environment_variables["csv_tmp_path"] = file_path
            environment_variables["csv_capture_path"] = path.join(file_path, "captures")
            environment_variables["csv_list_path"] = path.join(file_path, "lists")
            environment_variables["dns_request_files"] = file_path
            environment_variables["configuration_folder"] = path.join(frontend_folder, "local")

        return environment_variables

    @staticmethod
    def is_process_running(process_name) -> bool:
        return any(process.info["name"] in process_name
                   for process in psutil.process_iter(attrs=["name"]))
