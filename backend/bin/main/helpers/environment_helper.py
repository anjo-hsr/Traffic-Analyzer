from os import environ, path


class EnvironmentHelper:
    @staticmethod
    def get_environment():
        is_splunk_server = environ.get("SPLUNK_HOME")
        environment_variables = {}

        if is_splunk_server is not None:
            environment_variables["pcap_path"] = path.join("/tmp", "pcaps")
            environment_variables["csv_path"] = path.join("/tmp", "csvs")
            environment_variables["csv_enriched_path"] = path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer",
                                                                   "lookups")

        else:
            environment_variables["pcap_path"] = path.join("..", "..", "..", "docker", "init_files", "pcaps")
            environment_variables["csv_path"] = path.join("..", "files")
            environment_variables["csv_enriched_path"] = path.join("..", "files")

        return environment_variables
