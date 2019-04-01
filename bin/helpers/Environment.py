from os import environ, path


class Environment:
    @staticmethod
    def get_environment():
        environment_variables = {}

        if environ.get("SPLUNK_HOME") is not None:
            environment_variables["pcap_path"] = path.join("/tmp", "pcaps")
            environment_variables["csv_path"] = path.join("/tmp", "csvs")

        else:
            environment_variables["pcap_path"] = path.join("..", "docker", "init_files", "pcaps")
            environment_variables["csv_path"] = path.join(".", "files")

        return environment_variables
