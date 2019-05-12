from main.helpers.combine_helper import CombineHelper
from main.helpers.print_helper import PrintHelper


class NameResolverEnricher:
    def __init__(self):
        self.enricher_type = "name resolve enricher"
        self.header = "dst_fqdn,src_fqdn"

    def print(self):
        PrintHelper.print_nothing(self.enricher_type)

    @staticmethod
    def extract_fqdn(dst_src_information):
        dst_data = dst_src_information["dst"]
        src_data = dst_src_information["src"]
        fqdns = [dst_data["rdns"], src_data["rdns"]]
        return CombineHelper.delimiter.join('"{}"'.format(fqdn) for fqdn in fqdns)
