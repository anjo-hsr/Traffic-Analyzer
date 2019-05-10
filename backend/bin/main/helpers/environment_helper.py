from os import path

import psutil


class EnvironmentHelper:

    def __init__(self):
        self.production_process_name = "splunkd"

    def get_environment(self):
        is_splunk_server = self.check_process(self.production_process_name)

        environment_variables = {}

        if is_splunk_server:
            splunk_app_folder = path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer")
            splunk_app_lookup_folder = path.join(splunk_app_folder, "lookups")
            tmp_folder = "/tmp"

            environment_variables["pcap_path"] = path.join(tmp_folder, "pcaps")
            environment_variables["pcap_processed_path"] = path.join(tmp_folder, "pcaps_processed")
            environment_variables["csv_tmp_path"] = path.join(tmp_folder, "csvs")
            environment_variables["csv_capture_path"] = path.join(splunk_app_lookup_folder, "captures")
            environment_variables["csv_list_path"] = path.join(splunk_app_lookup_folder, "lists")
            environment_variables["dns_request_files"] = path.join(splunk_app_lookup_folder, "dns_request_files")
            environment_variables["configuration_folder"] = path.join(splunk_app_folder, "local")

        else:
            file_path = path.join("..", "files")
            docker_init_files_path = path.join("..", "..", "..", "docker", "init_files")

            environment_variables["pcap_path"] = path.join(docker_init_files_path, "pcaps")
            environment_variables["pcap_processed_path"] = path.join(docker_init_files_path, "pcaps")
            environment_variables["csv_tmp_path"] = file_path
            environment_variables["csv_capture_path"] = file_path
            environment_variables["csv_list_path"] = file_path
            environment_variables["dns_request_files"] = file_path
            environment_variables["configuration_folder"] = path.join("..", "..", "..", "frontend", "local")

        return environment_variables

    @staticmethod
    def check_process(process_name):
        for process in psutil.process_iter(attrs=["name"]):
            if process.info["name"] == process_name:
                return True
        return False
