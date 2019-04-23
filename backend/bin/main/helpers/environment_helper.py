from os import path

import psutil


class EnvironmentHelper:

    def __init__(self):
        self.production_process_name = "splunkd"
        self.splunk_app_folder = path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer")

    def get_environment(self):
        is_splunk_server = self.check_process(self.production_process_name)

        environment_variables = {}

        if is_splunk_server:
            environment_variables["pcap_path"] = path.join("/tmp", "pcaps")
            environment_variables["pcap_processed_path"] = path.join("/tmp", "pcaps_processed")
            environment_variables["csv_tmp_path"] = path.join("/tmp", "csvs")
            environment_variables["csv_capture_path"] = path.join(self.splunk_app_folder, "lookups", "captures")
            environment_variables["csv_list_path"] = path.join(self.splunk_app_folder, "lookups", "lists")

        else:
            environment_variables["pcap_path"] = path.join("..", "..", "..", "docker", "init_files", "pcaps")
            environment_variables["pcap_processed_path"] = path.join(
                "..", "..", "..", "docker", "init_files", "pcaps"
            )
            environment_variables["csv_tmp_path"] = path.join("..", "files")
            environment_variables["csv_capture_path"] = path.join("..", "files")
            environment_variables["csv_list_path"] = path.join("..", "files")

        return environment_variables

    @staticmethod
    def check_process(process_name):
        for process in psutil.process_iter(attrs=["name"]):
            if process.info["name"] == process_name:
                return True
        return False
