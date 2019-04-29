from IPy import IP


class IpHelper:
    def __init__(self):
        self.private_identifier = "PRIVATE"
        self.public_identifier = "PUBLIC"

    def is_private_ip(self, ip_addr):
        return IP(ip_addr).iptype() == self.private_identifier

    def is_public_ip(self, ip_addr):
        return IP(ip_addr).iptype() == self.public_identifier
