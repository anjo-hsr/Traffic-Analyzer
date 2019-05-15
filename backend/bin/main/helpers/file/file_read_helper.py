from csv import DictReader
from os import path

from main.helpers.environment_helper import EnvironmentHelper


def is_header(line_counter) -> bool:
    return line_counter == 0


def get_csv_dict_reader(csv_file) -> DictReader:
    return DictReader(csv_file, delimiter=',')


def get_config_value(config_name, key) -> str:
    environment = EnvironmentHelper().get_environment()
    file_path = path.join(environment["configuration_folder"], config_name)

    key_index = 0
    value_index = 1
    value = ""

    if path.isfile(file_path):
        with open(file_path) as config_file:
            for line in config_file:
                key_value = line.replace(" ", "").strip().split("=")
                if key_value[key_index] == key:
                    value = key_value[value_index]
                    break

    return value
