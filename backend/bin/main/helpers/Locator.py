import json
import requests
import socket

from main.helpers.ip_helper import IpHelper
from main.helpers.limiter import Limiter
from main.helpers.combiner import Combiner
from main.helpers.printer import Printer


class Locator:
    def __init__(self):
        self.locations = dict()
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"

    def print(self):
        print_text = "Print out for all {} location entries"
        Printer.print_dict(self.locations, print_text)

    def set_entry(self, ip_addr, lat_long):
        self.locations[ip_addr] = lat_long

    def get_location(self, ip_addr, limiter=Limiter(3, 1)):
        if ip_addr in self.locations:
            return

        if ip_addr == "" or not IpHelper.is_public_ip(ip_addr):
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
        pos_dest = Combiner.combine_lat_long(self.locations, destination)
        pos_src = Combiner.combine_lat_long(self.locations, source)

        return "{1}{0}{2}".format(Combiner.delimiter, pos_dest, pos_src)
