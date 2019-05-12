from main.enrichers.enricher import Enricher
from main.helpers.combine_helper import CombineHelper
from main.helpers.ip_helper import IpHelper


class IpTypeEnricher(Enricher):
    def __init__(self):
        enricher_type = "ip type enricher"
        header = "dst_is_private_ip,src_is_private_ip"
        Enricher.__init__(self, enricher_type, header)

        self.ip_dict = {}

    @staticmethod
    def extract_ip_types(dst_src_information) -> None:
        dst_ip = dst_src_information["dst"]["ip_address"]
        src_ip = dst_src_information["src"]["ip_address"]
        return CombineHelper.delimiter.join([IpTypeEnricher.is_private(dst_ip), IpTypeEnricher.is_private(src_ip)])

    @staticmethod
    def is_private(ip_address) -> str:
        ip_helper = IpHelper()
        is_private = False
        if ip_address != "":
            is_private = ip_helper.is_private_ip(ip_address)

        return str(is_private)
