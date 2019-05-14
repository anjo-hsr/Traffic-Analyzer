from main.enrichers.enricher import Enricher
from main.helpers.combine_helper import CombineHelper


class NameResolverEnricher(Enricher):
    def __init__(self):
        enricher_type = "name resolve enricher"
        header = "dst_fqdn,src_fqdn"
        Enricher.__init__(self, enricher_type, header)

    @staticmethod
    def extract_fqdn(dst_src_information) -> str:
        dst_data = dst_src_information["dst"]
        src_data = dst_src_information["src"]
        fqdns = [dst_data["rdns"], src_data["rdns"]]
        return CombineHelper.delimiter.join('"{}"'.format(fqdn) for fqdn in fqdns)
