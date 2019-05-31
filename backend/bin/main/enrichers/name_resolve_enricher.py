from main.enrichers.enricher import Enricher
from main.helpers.string_helper import enclose_with_quotes


class NameResolverEnricher(Enricher):
    def __init__(self):
        enricher_type = "name resolve enricher"
        header = "dst_fqdn,src_fqdn"
        Enricher.__init__(self, enricher_type, header)

    def get_information(self, _, information_dict) -> None:
        dst_data = information_dict["dst_src_information"]["dst"]
        src_data = information_dict["dst_src_information"]["src"]
        information_dict["dst_fqdn"] = enclose_with_quotes(dst_data["rdns"])
        information_dict["src_fqdn"] = enclose_with_quotes(src_data["rdns"])
