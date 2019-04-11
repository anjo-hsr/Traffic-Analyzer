import json
import socket

import requests

from main.helpers.ip_helper import IpHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper
from main.helpers.combine_helper import CombineHelper
from main.helpers.print_helper import PrintHelper


class LocationEnricher:
    def __init__(self):
        self.locations = dict()
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"

    def print(self):
        print_text = "Print out for all {} location entries"
        PrintHelper.print_dict(self.locations, print_text)

    def set_entry(self, ip_addr, lat_long):
        self.locations[ip_addr] = lat_long

    def get_location(self, ip_addr, limiter=TrafficLimitHelper(3, 1)):
        ip_helper = IpHelper()
        if ip_addr in self.locations:
            return

        if ip_addr == "" or not ip_helper.is_public_ip(ip_addr):
            lat_long = ["", ""]
            self.set_entry(ip_addr, lat_long)
            return

        limiter.check_request_load()

        try:
            lat_long = self.locate_ip(ip_addr)
            self.set_entry(ip_addr, lat_long)
        except socket.herror:
            pass

    def locate_ip(self, ip_addr):
        search_url = "https://tools.keycdn.com/geo.json?host={}".format(ip_addr)
        response = requests.get(search_url)
        response_json = json.loads(response.content.decode("utf-8"))
        data = response_json["data"]["geo"]
        lat_long = [data["latitude"], data["longitude"]]

        return lat_long

    def locate(self, dst_src):
        destination = dst_src["dst"]
        source = dst_src["src"]
        self.get_location(destination)
        self.get_location(source)
        pos_dest = CombineHelper.combine_lat_long(self.locations, destination)
        pos_src = CombineHelper.combine_lat_long(self.locations, source)

        return "{1}{0}{2}".format(CombineHelper.delimiter, pos_dest, pos_src)
