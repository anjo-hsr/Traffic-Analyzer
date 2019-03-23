import socket
import csv
import requests
import json
import time
from IPy import IP
from bin import Limiter


def is_header(line_number):
    return line_number == 0


def check_request_load(limiter):
    current_time = Limiter.get_current_timestamp()
    limiter.increase_counter()
    waiting_time = limiter.get_period_time() - (current_time - limiter.get_period_timestamp())

    if (limiter.counter == limiter.requests_per_period) and waiting_time > 0:
        time.sleep(waiting_time)
        limiter.reset_period_timestamp()

    if waiting_time < 0:
        limiter.reset_period_timestamp()


def get_locations(locations, limiter, packet):
    src_ip = packet[4]
    dst_ip = packet[5]
    get_location(locations, limiter, src_ip)
    get_location(locations, limiter, dst_ip)


def set_lat_long(locations, ip_addr, lat_long):
    locations[ip_addr] = lat_long


def is_public_ip(ip_addr):
    return IP(ip_addr).iptype() == "PUBLIC"


def get_location(locations, limiter, ip_addr):
    if ip_addr in locations:
        return

    if ip_addr == "" or not is_public_ip(ip_addr):
        lat_long = ["", ""]
        set_lat_long(locations, ip_addr, lat_long)
        return

    check_request_load(limiter)

    try:
        search_url = "https://tools.keycdn.com/geo.json?host=" + ip_addr
        response = requests.get(search_url)
        response_json = json.loads(response.content)
        geo = response_json["data"]["geo"]
        lat_long = [geo["latitude"], geo["longitude"]]
        set_lat_long(locations, ip_addr, lat_long)
    except socket.herror:
        pass


def main():
    with open('test.csv', mode="r", encoding='utf-8') as capture:
        locations = dict()
        limiter = Limiter.Limiter(3, 1)

        capture_reader = csv.reader(capture, delimiter=',')
        line_counter = 0

        for packet in capture_reader:
            if not is_header(line_counter):
                get_locations(locations, limiter, packet)

            line_counter += 1

    for location in locations:
        print(location + " --> " + str(locations[location]))


main()
