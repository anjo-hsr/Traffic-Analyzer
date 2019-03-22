import socket
import csv
import requests
import json


def is_header(line_number):
    return line_number == 0


def get_locations():
    src_ip = packet[0]
    dst_ip = packet[1]
    get_location(src_ip)
    get_location(dst_ip)


def get_location(ip_addr):
    if ip_addr in locations:
        return

    try:
        search_url = "https://tools.keycdn.com/geo.json?host=" + ip_addr
        response = requests.get(search_url)
        response_json = json.loads(response.content)
        latitude = response_json["data"]["geo"]["latitude"]
        longitude = response_json["data"]["geo"]["longitude"]
        locations[ip_addr] = [latitude, longitude]
    except socket.herror:
        pass


with open('ips.csv', mode="r", encoding='utf-8') as capture:
    locations = dict()

    capture_reader = csv.reader(capture, delimiter=',')
    line_counter = 0
    for packet in capture_reader:
        if not is_header(line_counter):
            get_locations()

        line_counter += 1

for location in locations:
    print(location + " --> " + str(locations[location]))
