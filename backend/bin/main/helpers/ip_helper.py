import ipaddress


class IpHelper:
    @staticmethod
    def is_public_ip(ip_addr):
        try:
            # Double check must be made because ipaddress classifies 224.0.0.1 as a global address which would then be
            # searched over nslookup.
            # https://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml#multicast-addresses-1
            return ipaddress.ip_address(ip_addr).is_global and \
                   not ipaddress.ip_address(ip_addr).is_multicast
        except ValueError:
            return False

    @staticmethod
    def is_ip(ip_addr):
        try:
            ipaddress.ip_address(ip_addr)
            return True
        except ValueError:
            return False
