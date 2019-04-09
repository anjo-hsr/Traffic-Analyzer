import re

from os import path

import main.helpers.FileHelper as FileHelper


def convert_mac_address(row):
    vendor_part = row["Assignment"].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


def write_row(output_file, row):
    mac_address = convert_mac_address(row)
    line = mac_address + "," + '"{}"'.format(row["Organization Name"])
    FileHelper.write_line(output_file, line)


def main():
    destination_file = path.join("..", "..", "files", "mac_vendor.csv")
    run(destination_file)


def run(destination_file):
    url = "http://standards-oui.ieee.org/oui/oui.csv"
    filename = FileHelper.download_file(url)

    with \
            open(filename, mode="r", encoding='utf-8') as csv_file, \
            open(destination_file, mode='w', encoding='utf-8') as output_file:
        header = "eth_short,vendor"
        FileHelper.write_download_file(write_row, csv_file, output_file, header)

    FileHelper.remove_file(filename)


if __name__ == "__main__":
    main()
