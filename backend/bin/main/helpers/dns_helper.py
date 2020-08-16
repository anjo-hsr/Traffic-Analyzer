import time

from dns import exception, resolver, reversename

from main.helpers.file import file_read_helper
from main.helpers.ip_address_helper import IpAddressHelper
from main.helpers.string_helper import remove_spaces


class DnsHelper(object):
    def __init__(self) -> None:
        self.dns_resolver = resolver.Resolver()
        self.dns_resolver_tester = resolver.Resolver()
        self.set_dns_resolver()

    def set_dns_resolver(self, dns_lifetime: int = 2) -> None:
        self.set_lifetime(dns_lifetime)
        self.set_dns_server()

    def set_lifetime(self, dns_lifetime: int) -> None:
        self.dns_resolver.lifetime = dns_lifetime
        self.dns_resolver_tester.lifetime = dns_lifetime

    def set_dns_server(self) -> None:
        config_name = "traffic-analyzer.conf"
        key = "internal_dns_servers"
        dns_servers = file_read_helper.get_config_value(config_name, key)
        dns_servers = remove_spaces(dns_servers)
        for dns_server in dns_servers.split(","):
            if self.check_dns_server_entry(dns_server):
                self.dns_resolver.nameservers.append(dns_server)

    def check_dns_server_entry(self, dns_server: str) -> bool:
        if dns_server == "":
            return False

        return self.is_dns_server_available(dns_server)

    def reset_dns_resolver(self, dns_lifetime: int = 2) -> None:
        self.dns_resolver.__init__()
        self.set_lifetime(dns_lifetime)

    def is_dns_server_available(self, dns_server_address: str) -> bool:
        self.dns_resolver_tester.nameservers = [dns_server_address]
        try:
            if IpAddressHelper.is_ip(dns_server_address):
                dns_server_address = reversename.from_address(dns_server_address)
            self.dns_resolver_tester.query(dns_server_address, "PTR")
            return True

        except exception.Timeout:
            return False

    def get_fqdn(self, ip_address: str, counter: int = 0) -> str:
        fqdn = ip_address
        try:
            in_addr_arpa_address = reversename.from_address(ip_address)
            fqdn = str(self.dns_resolver.query(in_addr_arpa_address, "PTR")[0])

        except exception.Timeout:
            if counter < 5:
                time.sleep(2)
                self.get_fqdn(ip_address, counter + 1)

            self.reset_dns_resolver()

        except (resolver.NXDOMAIN, resolver.NoNameservers, resolver.NoAnswer):
            # Let pass if the server has no reverse lookup zone for the specified ip address or the ip was
            # not found in the reverse lookup zone.
            pass

        return fqdn
