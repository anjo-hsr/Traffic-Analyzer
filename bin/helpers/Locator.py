from bin.helpers.IPHelper import IPHelper
from bin.helpers.Limiter import Limiter
from bin.helpers.Combiner import Combiner

import json
import requests
import socket


class Locator:
    def __init__(self):
        self.locations = dict()
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"

    def print_fqdns(self):
        print("Print out for all {} location entries".format(self.locations.__len__()))
        for location_entry in self.locations:
            print("{} --> {}".format(location_entry, self.locations[location_entry]))

        print("\n\n")

    def set_entry(self, ip_addr, lat_long):
        self.locations[ip_addr] = lat_long

    def get_location(self, limiter, ip_addr):
        if ip_addr in self.locations:
            return

        if ip_addr == "" or not IPHelper.is_public_ip(ip_addr):
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
        search_url = "https://tools.keycdn.com/geo.json?host=" + ip_addr
        response = requests.get(search_url)
        response_json = json.loads(response.content)
        geo = response_json["data"]["geo"]
        lat_long = [geo["latitude"], geo["longitude"]]
        return lat_long

    def locate(self, dst_src):
        destination = dst_src[0]
        source = dst_src[1]
        limiter = Limiter(3, 1)
        self.get_location(limiter, destination)
        self.get_location(limiter, source)
        pos_dest = Combiner.combine_lat_long(self.locations, destination)
        pos_src = Combiner.combine_lat_long(self.locations, source)

        return "{1}{0}{2}".format(Combiner.delimiter, pos_dest, pos_src)


