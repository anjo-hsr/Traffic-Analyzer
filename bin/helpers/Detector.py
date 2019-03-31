import os


class Detector:
    @staticmethod
    def get_environment():
        environment_variables = {}

        if not os.environ['SPLUNK_HOME'] is None:
            environment_variables["pcap_path"] = os.path.join("/tmp", "pcaps")
            environment_variables["csv_path"] = os.path.join("/tmp", "csvs")

        else:
            environment_variables["pcap_path"] = os.path.join("..", "docker", "init_files", "pcaps")
            environment_variables["csv_path"] = os.path.join(".", "files")

        return environment_variables
