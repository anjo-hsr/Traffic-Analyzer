import urllib.request
import csv
import re

url = "http://standards-oui.ieee.org/oui/oui.csv"

file_name = url.split("/")[-1]

urllib.request.urlretrieve(url, file_name)

mac_vendor = dict()
with \
        open(file_name, mode="r", encoding='utf-8') as csv_file,\
        open('test2.csv', 'w', encoding='utf-8') as output_file:
    output_file.write("eth_short,vendor\n")
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            row[1] = row[1].lower()
            mac_address_array = re.findall("..?", row[1])
            mac_address = ":".join(mac_address_array)
            output_file.write(mac_address + ',"' + row[2] + '"\n')
        line_count += 1