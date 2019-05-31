from main.enrichers.enricher import Enricher
from main.helpers.ip_helper import IpHelper


class IpTypeEnricher(Enricher):
    def __init__(self):
        enricher_type = "ip type enricher"
        header = "dst_is_private_ip,src_is_private_ip"
        Enricher.__init__(self, enricher_type, header)

        self.ip_dict = {}

    def get_information(self, _, information_dict) -> None:
        dst_ip = information_dict["dst_src_information"]["dst"]["ip_address"]
        src_ip = information_dict["dst_src_information"]["src"]["ip_address"]

        information_dict["dst_is_private_ip"] = IpTypeEnricher.is_private(dst_ip)
        information_dict["src_is_private_ip"] = IpTypeEnricher.is_private(src_ip)

    @staticmethod
    def is_private(ip_address) -> str:
        is_private = False
        if ip_address != "":
            is_private = IpHelper.is_private_ip(ip_address)

        return str(is_private)
