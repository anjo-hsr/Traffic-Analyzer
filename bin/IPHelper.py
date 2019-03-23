from IPy import IP


class IPHelper:

    @staticmethod
    def is_public_ip(ip_addr):
        return IP(ip_addr).iptype() == "PUBLIC"
