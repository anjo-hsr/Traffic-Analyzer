import csv
import re

from os import path, remove
from urllib import request

from main.helpers import FileDownloader


def download_file(mac_vendor_url):
    file_name = mac_vendor_url.split("/")[-1]
    request.urlretrieve(mac_vendor_url, file_name)
    return file_name


def is_header(line_counter):
    return line_counter == 0


def convert_mac_address(row):
    vendor_part = row["Assignment"].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


def write_rows(line_counter, output_file, row):
    if not is_header(line_counter):
        mac_address = convert_mac_address(row)
        write_line(output_file, mac_address + "," + '"{}"'.format(row["Organization Name"]))
    return line_counter + 1


def write_line(output_file, line):
    output_file.write(line + "\n")


def main():
    url = "http://standards-oui.ieee.org/oui/oui.csv"
    file_name = FileDownloader.download_file(url)
    destination_file = path.join("..", "files", "mac_vendor.csv")

    with \
            open(file_name, mode="r", encoding='utf-8') as csv_file, \
            open(destination_file, mode='w', encoding='utf-8') as output_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        write_line(output_file, "eth_short,vendor")
        line_counter = 0
        for row in csv_reader:
            line_counter = write_rows(line_counter, output_file, row)

    remove(file_name)


if __name__ == "__main__":
    main()
