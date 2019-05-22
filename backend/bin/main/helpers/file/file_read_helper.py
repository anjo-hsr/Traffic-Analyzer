import hashlib
from csv import DictReader
from os import path
from typing import List

from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.print_helper import PrintHelper


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

    if not path.isfile(file_path):
        return value

    with open(file_path) as config_file:
        for line in config_file:
            key_value = line.replace(" ", "").strip().split("=")
            if key_value[key_index] == key:
                value = key_value[value_index]
                break

        return value


def get_file_hashes(hash_path) -> List[str]:
    if not path.isfile(hash_path):
        return []

    return [line.replace("\n", "") for line in list(open(hash_path))]


def get_file_hashsum(file_path, block_size=65536) -> str:
    if not path.isfile(file_path):
        print_text = "File not found"
        PrintHelper.print_error(print_text)
        return ""

    hash_function = hashlib.sha256()
    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(block_size), b''):
            hash_function.update(block)

        return hash_function.hexdigest()
