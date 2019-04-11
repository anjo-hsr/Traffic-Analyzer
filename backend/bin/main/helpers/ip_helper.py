from IPy import IP


class IpHelper(object):
    def __init__(self):
        self.public_identifier = "PUBLIC"

    def is_public_ip(self, ip_addr):
        return IP(ip_addr).iptype() == self.public_identifier
