import ipaddress


class IpHelper:
    @staticmethod
    def is_public_ip(ip_addr):
        try:
            return ipaddress.ip_address(ip_addr).is_global
        except ValueError:
            return False

    @staticmethod
    def is_ip(ip_addr):
        try:
            ipaddress.ip_address(ip_addr)
            return True
        except ValueError:
            return False
