import json
import requests
import socket

from main.helpers.IPHelper import IPHelper
from main.helpers.Limiter import Limiter
from main.helpers.Combiner import Combiner


class Locator:
    def __init__(self):
        self.locations = dict()
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"

    def print(self):
        print("Print out for all {} location entries".format(len(self.locations)))
        for location_entry in self.locations:
            print("{} --> {}".format(location_entry, self.locations[location_entry]))

        print("\n\n")

    def set_entry(self, ip_addr, lat_long):
        self.locations[ip_addr] = lat_long

    def get_location(self, ip_addr, limiter=Limiter(3, 1)):
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
        search_url = "https://geoip-db.com/json/{}".format(ip_addr)
        response = requests.get(search_url)
        response_json = json.loads(response.content.decode("utf-8"))
        lat_long = [response_json["latitude"], response_json["longitude"]]

        return lat_long

    def locate(self, dst_src):
        destination = dst_src["dst"]
        source = dst_src["src"]
        self.get_location(destination)
        self.get_location(source)
        pos_dest = Combiner.combine_lat_long(self.locations, destination)
        pos_src = Combiner.combine_lat_long(self.locations, source)

        return "{1}{0}{2}".format(Combiner.delimiter, pos_dest, pos_src)
