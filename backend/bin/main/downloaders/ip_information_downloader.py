import json
import socket
import time
from typing import Dict

import requests
from dns import resolver, reversename, exception

from main.helpers.file import file_read_helper
from main.helpers.ip_address_helper import IpAddressHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class IpInformationDownloader:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)) -> None:
        self.ip_information = {}
        self.limiter = limiter
        self.dns_resolver = resolver.Resolver()

        self.set_dns_resolver()

    def set_dns_resolver(self, dns_lifetime=2) -> None:
        self.dns_resolver.lifetime = dns_lifetime
        self.set_dns_server()

    def set_dns_server(self) -> None:
        config_name = "traffic-analyzer.conf"
        key = "internal_dns_server"
        dns_server = file_read_helper.get_config_value(config_name, key)
        self.check_dns_server_entry(dns_server)

    def check_dns_server_entry(self, dns_server):
        self.dns_resolver.nameservers = [dns_server]
        if not self.is_dns_server_avaiable(dns_server):
            self.reser_dns_server()

    def reser_dns_server(self):
        self.dns_resolver.nameservers = []

    def is_dns_server_avaiable(self, dns_server_address):
        try:
            if IpAddressHelper.is_ip(dns_server_address):
                dns_server_address = reversename.from_address(dns_server_address)
            self.dns_resolver.query(dns_server_address, "PTR")
            return True

        except exception.Timeout:
            return False

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

        if ip_address == "" or not IpAddressHelper.is_global_ip(ip_address):
            self.ip_information[ip_address] = self.get_private_ip_data(ip_address)
            return

        self.limiter.check_request_load()
        self.ip_information[ip_address] = self.get_ip_data(ip_address)

    def get_ip_data(self, ip_addr, counter=0) -> Dict[str, str]:
        try:
            search_url = "https://tools.keycdn.com/geo.json?host={}".format(ip_addr)
            response = requests.get(search_url)
            if response.status_code == 200:
                response_json = json.loads(response.content.decode("utf-8"))
                geo_data = response_json["data"]["geo"]
                return self.extract_data(geo_data, ip_addr)

        except socket.gaierror:
            if counter < 5:
                time.sleep(2)
                IpInformationDownloader.get_ip_data(ip_addr, counter + 1)

        return self.get_private_ip_data(ip_addr)

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

    def get_private_ip_data(self, ip_address) -> Dict[str, str]:
        fqdn = ip_address
        if ip_address != "" and IpAddressHelper.is_private_ip(ip_address):
            fqdn = self.get_fqdn(fqdn, ip_address)

        return {
            "ip_address": ip_address,
            "rdns": fqdn,
            "asn": "",
            "isp": "",
            "latitude": "",
            "longitude": ""
        }

    def get_fqdn(self, fqdn, ip_address, counter=0) -> str:
        try:
            in_addr_arpa_address = reversename.from_address(ip_address)
            fqdn = str(self.dns_resolver.query(in_addr_arpa_address, "PTR")[0])

        except exception.Timeout:
            if counter < 5:
                time.sleep(2)
                self.get_fqdn(fqdn, ip_address, counter + 1)

            self.reser_dns_server()

        except (resolver.NXDOMAIN, resolver.NoNameservers):
            # Let pass if the server has no reverse lookup zone for the specified ip address or the ip was
            # not found in the reverse lookup zone.
            pass

        return fqdn
