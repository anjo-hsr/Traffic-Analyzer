import socket

from main.helpers.combine_helper import CombineHelper
from main.helpers.ip_helper import IpHelper
from main.helpers.print_helper import PrintHelper


class NameResolverEnricher:
    def __init__(self):
        self.fqdns = dict()
        self.header = "dst_fqdn,src_fqdn"

    def print(self):
        print_text = "Print out for {} fqdn entries"
        PrintHelper.print_dict(self.fqdns, print_text)

    def get_fqdn(self, ip_addr):
        if ip_addr in self.fqdns:
            return

        if ip_addr == "" or not IpHelper.is_global_ip(ip_addr):
            self.set_entry(ip_addr, ip_addr)
            return

        try:
            fqdn = socket.getfqdn(ip_addr)
            self.set_entry(ip_addr, fqdn)
        except socket.herror:
            pass

    def set_entry(self, ip_addr, fqdn):
        self.fqdns[ip_addr] = fqdn

    def resolve(self, dst_src):
        destination = dst_src["dst"]
        source = dst_src["src"]

        self.get_fqdn(destination)
        self.get_fqdn(source)
        return CombineHelper.combine_fqdns(self.fqdns, destination, source)
