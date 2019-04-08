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
    url = "http://standards-oui.ieee.org/oui/oui.csv"
    filename = FileHelper.download_file(url)
    destination_file = path.join("..", "..", "files", "mac_vendor.csv")

    with \
            open(filename, mode="r", encoding='utf-8') as csv_file, \
            open(destination_file, mode='w', encoding='utf-8') as output_file:
        csv_reader = FileHelper.get_csv_dict_reader(csv_file)

        header = "eth_short,vendor"
        FileHelper.write_line(output_file, header)

        for row in csv_reader:
            write_row(output_file, row)

    FileHelper.remove_file(filename)


if __name__ == "__main__":
    main()
