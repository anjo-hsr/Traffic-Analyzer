from main.helpers.combine_helper import CombineHelper
from main.helpers.ip_helper import IpHelper
from main.helpers.print_helper import PrintHelper


class IpTypeEnricher:
    def __init__(self):
        self.header = "dst_is_private_ip,src_is_private_ip"
        self.enricher_type = "ip_type_enricher"
        self.ip_dict = {}

    def print(self):
        PrintHelper.print_nothing(self.enricher_type)

    @staticmethod
    def extract_ip_types(dst_src_information):
        dst_ip = dst_src_information["dst"]["ip_address"]
        src_ip = dst_src_information["src"]["ip_address"]
        return CombineHelper.delimiter.join([IpTypeEnricher.is_private(dst_ip), IpTypeEnricher.is_private(src_ip)])

    @staticmethod
    def is_private(ip_address):
        ip_helper = IpHelper()
        is_private = False
        if ip_address != "":
            is_private = ip_helper.is_private_ip(ip_address)

        return str(is_private)
