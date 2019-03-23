import socket
import csv
from IPy import IP


def is_header(line_number):
    return line_number == 0


def is_public_ip(ip_addr):
    return IP(ip_addr).iptype() == "PUBLIC"


def get_fqdns(fqdns, packet):
    src_ip = packet[4]
    dst_ip = packet[5]
    get_fqdn(fqdns, src_ip)
    get_fqdn(fqdns, dst_ip)


def get_fqdn(fqdns, ip_addr):
    if ip_addr in fqdns:
        return

    if ip_addr == "" or not is_public_ip:
        fqdns[ip_addr] = ip_addr
        return

    try:
        fqdns[ip_addr] = socket.getfqdn(ip_addr)
    except socket.herror:
        pass


def main():
    with \
            open('test.csv', mode="r", encoding='utf-8') as capture, \
            open('fqdns.csv', 'w', encoding='utf-8') as output_file:
        fqdns = dict()
        capture_reader = csv.reader(capture, delimiter=',')
        line_counter = 0
        for packet in capture_reader:
            joined_cells = ','.join('"{}"'.format(cell) for cell in packet)
            if is_header(line_counter):
                write_line(output_file, joined_cells + ",src_fqdn,dst_fqdn")

            else:
                get_fqdns(fqdns, packet)
                src_dst_fqdns = "{},{}".format(fqdns.get(packet[4]), fqdns.get(packet[5]))
                write_line(output_file, joined_cells + "," + src_dst_fqdns)
            line_counter += 1

    for location in fqdns:
        print(location + " --> " + fqdns[location])


def write_line(output_file, line):
    output_file.write(line + "\n")


main()
