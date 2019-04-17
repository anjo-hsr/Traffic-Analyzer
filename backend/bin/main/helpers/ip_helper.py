import ipaddress


class IpHelper:
    @staticmethod
    def is_global_ip(ip_address):
        try:
            ip = ipaddress.ip_address(ip_address)

            # Multicast addresses are currently detected as globally addresses. To prevent this false positive
            # the check for is_global is done with multiple checks.
            return not (ip.is_multicast or ip.is_private or ip.is_loopback)
        except ValueError:
            return False

    @staticmethod
    def is_ip(ip_address):
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
