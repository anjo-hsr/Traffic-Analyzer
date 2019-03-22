import urllib.request
import csv
import re


def download_file(mac_vendor_url):
    file_name = mac_vendor_url.split("/")[-1]
    urllib.request.urlretrieve(mac_vendor_url, file_name)
    return file_name


def is_header(line_counter):
    return line_counter == 0


def convert_mac_address(row):
    vendor_part = row[1].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


def write_rows(line_counter, output_file, row):
    if not is_header(line_counter):
        mac_address = convert_mac_address(row)
        write_line(output_file, mac_address + ',"' + row[2] + '"\n')
    return line_counter + 1


def write_line(output_file, line):
    output_file.write()


def main():
    mac_vendor_url = "http://standards-oui.ieee.org/oui/oui.csv"
    file_name = download_file(mac_vendor_url)

    with \
            open(file_name, mode="r", encoding='utf-8') as csv_file, \
            open('test2.csv', 'w', encoding='utf-8') as output_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        write_line(output_file, "eth_short,vendor\n")
        line_counter = 0
        for row in csv_reader:
            line_counter = write_rows(line_counter, output_file, row)


main()
