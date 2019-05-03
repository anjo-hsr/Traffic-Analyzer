import ipaddress


class IpHelper:
    @staticmethod
    def is_global_ip(ip_address):
        try:
            ip = ipaddress.ip_address(ip_address)

            # Multicast addresses are in ipaddress detected as globally addresses. The function is used to tell if a IP
            # address should be resolved with nslookup. This line prevents the checking of multicast ips as well.
            return ip.is_global and not ip.is_multicast
        except ValueError:
            return False

    @staticmethod
    def is_multicast_ip(ip_address):
        try:
            ip = ipaddress.ip_address(ip_address)
            return ip.is_multicast
        except ValueError:
            return False

    @staticmethod
    def is_private_ip(ip_address):
        try:
            ip = ipaddress.ip_address(ip_address)
            return ip.is_private
        except ValueError:
            return False

    @staticmethod
    def is_ip(ip_address):
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
