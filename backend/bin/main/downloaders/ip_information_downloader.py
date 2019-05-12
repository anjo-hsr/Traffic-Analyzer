import json
import socket
import time
from typing import Dict

import requests

from main.helpers.ip_helper import IpHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class IpInformationDownloader:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)):
        self.ip_information = {}
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"
        self.limiter = limiter

    def get_dst_src_information(self, dst_src) -> Dict[str, str]:
        dst = dst_src["dst"]
        src = dst_src["src"]
        self.get_ip_information(dst)
        self.get_ip_information(src)
        return {
            "dst": self.ip_information[dst],
            "src": self.ip_information[src]
        }

    def get_ip_information(self, ip_address) -> None:
        if ip_address in self.ip_information:
            return

        if ip_address == "" or not IpHelper.is_global_ip(ip_address):
            self.ip_information[ip_address] = IpInformationDownloader.get_private_ip_data(ip_address)
            return

        self.limiter.check_request_load()
        self.ip_information[ip_address] = self.get_ip_data(ip_address)

    @staticmethod
    def get_fqdn(fqdn, ip_address) -> str:
        try:
            fqdn = socket.getfqdn(ip_address)
        except socket.herror:
            pass
        return fqdn

    @staticmethod
    def get_ip_data(ip_addr, counter=0) -> Dict[str, str]:
        try:
            search_url = "https://tools.keycdn.com/geo.json?host={}".format(ip_addr)
            response = requests.get(search_url)
            response_json = json.loads(response.content.decode("utf-8"))
            geo_data = response_json["data"]["geo"]
            return ip_addr.extract_data(geo_data, ip_addr)

        except socket.gaierror:
            if counter < 5:
                time.sleep(2)
                IpInformationDownloader.get_ip_data(ip_addr, counter + 1)

            return IpInformationDownloader.get_private_ip_data(ip_addr)

    @staticmethod
    def extract_data(geo_data, ip_addr) -> Dict[str, str]:
        return {
            "ip_address": ip_addr,
            "rdns": geo_data["rdns"],
            "asn": geo_data["asn"],
            "isp": geo_data["isp"],
            "latitude": geo_data["latitude"],
            "longitude": geo_data["longitude"],
        }

    @staticmethod
    def get_private_ip_data(ip_address) -> Dict[str, str]:
        fqdn = ip_address
        if ip_address != "" and IpHelper.is_private_ip(ip_address):
            fqdn = IpInformationDownloader.get_fqdn(fqdn, ip_address)

        return {
            "ip_address": ip_address,
            "rdns": fqdn,
            "asn": "",
            "isp": "",
            "latitude": "",
            "longitude": ""
        }