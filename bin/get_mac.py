import urllib.request
import csv
import re


def is_header():
    return line_counter == 0


def convert_mac_address():
    vendor_part = row[1].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


mac_vendor_url = "http://standards-oui.ieee.org/oui/oui.csv"
file_name = mac_vendor_url.split("/")[-1]
urllib.request.urlretrieve(mac_vendor_url, file_name)

with \
        open(file_name, mode="r", encoding='utf-8') as csv_file, \
        open('test2.csv', 'w', encoding='utf-8') as output_file:
    mac_vendor = dict()
    csv_reader = csv.reader(csv_file, delimiter=',')

    output_file.write("eth_short,vendor\n")
    line_counter = 0
    for row in csv_reader:
        if not is_header():
            mac_address = convert_mac_address()
            output_file.write(mac_address + ',"' + row[2] + '"\n')
        line_counter += 1
