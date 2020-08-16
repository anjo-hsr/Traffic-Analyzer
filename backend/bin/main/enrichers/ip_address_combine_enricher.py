from typing import Dict, Optional, Union

from main.enrichers.enricher import Enricher


class IpAddressCombineEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "ip address combine enricher"
        header = "ip_src_combined,ip_dst_combined"
        Enricher.__init__(self, enricher_type, header)

        self.ip_dict = {}

    def get_information(self, _: Optional[Dict[str, str]],
                        information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        information_dict["ip_dst_combined"] = information_dict["dst_src_information"]["dst"]["ip_address"]
        information_dict["ip_src_combined"] = information_dict["dst_src_information"]["src"]["ip_address"]
