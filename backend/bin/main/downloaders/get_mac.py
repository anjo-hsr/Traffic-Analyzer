import re

from os import path

import main.downloaders.download_methods as download_methods


def convert_mac_address(row):
    vendor_part = row["Assignment"].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


def write_row(output_file, row):
    mac_address = convert_mac_address(row)
    line = mac_address + "," + '"{}"'.format(row["Organization Name"])
    download_methods.write_line(output_file, line)


def main():
    url = "http://standards-oui.ieee.org/oui/oui.csv"
    filename = download_methods.download_file(url)
    destination_file = path.join("..", "..", "files", "mac_vendor.csv")

    with \
            open(filename, mode="r", encoding='utf-8') as csv_file, \
            open(destination_file, mode='w', encoding='utf-8') as output_file:
        csv_reader = download_methods.get_csv_dict_reader(csv_file)

        header = "eth_short,vendor"
        download_methods.write_line(output_file, header)

        for row in csv_reader:
            write_row(output_file, row)

    download_methods.remove_downloaded_file(filename)


if __name__ == "__main__":
    main()
