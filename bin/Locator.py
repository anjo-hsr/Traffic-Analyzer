import socket
import requests
import json
import time
from bin import Limiter
from bin.IPHelper import IPHelper


class Locator:
    def __init__(self):
        self.locations = dict()
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"

    def check_request_load(self, limiter):
        current_time = Limiter.get_current_timestamp()
        limiter.increase_counter()
        waiting_time = limiter.get_period_time() - (current_time - limiter.get_period_timestamp())

        if (limiter.counter == limiter.requests_per_period) and waiting_time > 0:
            time.sleep(waiting_time)
            limiter.reset_period_timestamp()

        if waiting_time < 0:
            limiter.reset_period_timestamp()

    def set_entry(self, ip_addr, lat_long):
        self.locations[ip_addr] = lat_long

    def get_location(self, limiter, ip_addr):
        if ip_addr in self.locations:
            return

        if ip_addr == "" or not IPHelper.is_public_ip(ip_addr):
            lat_long = ["", ""]
            self.set_entry(ip_addr, lat_long)
            return

        self.check_request_load(limiter)

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

        limiter = Limiter.Limiter(3, 1)
        self.get_location(limiter, destination)
        self.get_location(limiter, source)
        pos_dest = ','.join('"{}"'.format(cell) for cell in self.locations.get(destination))
        pos_src = ','.join('"{}"'.format(cell) for cell in self.locations.get(source))

        return "{},{}".format(pos_dest, pos_src)
