from os import environ, path


class EnvironmentHelper:

    def __init__(self):
        self.production_env_identifier = "SPLUNK_HOME"

    def get_environment(self):
        is_splunk_server = environ.get(self.production_env_identifier)
        environment_variables = {}

        if is_splunk_server is not None:
            environment_variables["pcap_path"] = path.join("/tmp", "pcaps")
            environment_variables["csv_path"] = path.join("/tmp", "csvs")
            environment_variables["csv_enriched_path"] = path.join(
                "/opt", "splunk", "etc", "apps", "traffic-analyzer", "lookups"
            )

        else:
            environment_variables["pcap_path"] = path.join("..", "..", "..", "docker", "init_files", "pcaps")
            environment_variables["csv_path"] = path.join("..", "files")
            environment_variables["csv_enriched_path"] = path.join("..", "files")

        return environment_variables
