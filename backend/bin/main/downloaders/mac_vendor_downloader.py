import re

from os import path

import main.helpers.file_helper as file_helper

from main.helpers.environment_helper import EnvironmentHelper


def convert_mac_address(row):
    vendor_part = row["Assignment"].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


def write_row(output_file, row):
    mac_address = convert_mac_address(row)
    line = mac_address + "," + '"{}"'.format(row["Organization Name"])
    file_helper.write_line(output_file, line)


def main():
    environment_helper = EnvironmentHelper()
    environment_variables = environment_helper.get_environment()
    destination_mac_csv = path.join(environment_variables["csv_list_path"], "mac_vendor.csv")
    run(destination_mac_csv)


def run(destination_file):
    url = "http://standards-oui.ieee.org/oui/oui.csv"
    filename = file_helper.download_file(url)

    with \
            open(filename, mode="r", encoding='utf-8') as csv_file, \
            open(destination_file, mode='w', encoding='utf-8') as output_file:
        header = "eth_short,vendor"
        file_helper.write_download_file(write_row, csv_file, output_file, header)

    file_helper.remove_file(filename)


if __name__ == "__main__":
    main()
