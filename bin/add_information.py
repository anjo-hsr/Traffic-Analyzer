from bin.Locator import Locator
from bin.NameResolver import NameResolver
import csv


def is_header(line_number):
    return line_number == 0


def write_line(output_file, line):
    output_file.write(line + "\n")


def combine_information(joined_default_cells, header_fqdn, header_location):
    return "{},{},{}".format(joined_default_cells, header_fqdn, header_location)


def main():
    locator = Locator()
    name_resolver = NameResolver()

    with \
            open('test.csv', mode="r", encoding='utf-8') as capture, \
            open('enriched.csv', 'w', encoding='utf-8') as output_file:
        csv_reader = csv.reader(capture, delimiter=',')
        for index, packet in enumerate(csv_reader):
            joined_default_cells = ','.join('"{}"'.format(cell) for cell in packet)
            if is_header(index):
                fqdn_header = name_resolver.header
                location_header = locator.header
                line = combine_information(joined_default_cells, fqdn_header, location_header)

            else:
                dst_ip_addr = packet[4]
                src_ip_addr = packet[5]
                src_dst = [dst_ip_addr, src_ip_addr]
                fqdn_information = name_resolver.resolve(src_dst)
                location_information = locator.locate(src_dst)
                line = combine_information(joined_default_cells, fqdn_information, location_information)

            write_line(output_file, line)


main()
