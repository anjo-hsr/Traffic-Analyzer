from main.enrichers.enricher import Enricher


class IpAddressCombineEnricher(Enricher):
    def __init__(self):
        enricher_type = "ip address combine enricher"
        header = "ip_src_combined,ip_dst_combined"
        Enricher.__init__(self, enricher_type, header)

        self.ip_dict = {}

    def get_information(self, _, information_dict) -> None:
        information_dict["ip_dst_combined"] = information_dict["dst_src_information"]["dst"]["ip_address"]
        information_dict["ip_src_combined"] = information_dict["dst_src_information"]["src"]["ip_address"]
