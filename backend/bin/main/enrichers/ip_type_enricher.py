from typing import Dict, Union, Optional

from main.enrichers.enricher import Enricher
from main.helpers.ip_address_helper import IpAddressHelper


class IpTypeEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "ip type enricher"
        header = "dst_is_private_ip,src_is_private_ip"
        Enricher.__init__(self, enricher_type, header)

        self.ip_dict = {}

    def get_information(self, _: Optional[Dict[str, str]],
                        information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        dst_ip = information_dict["dst_src_information"]["dst"]["ip_address"]
        src_ip = information_dict["dst_src_information"]["src"]["ip_address"]

        information_dict["dst_is_private_ip"] = IpTypeEnricher.is_private(dst_ip)
        information_dict["src_is_private_ip"] = IpTypeEnricher.is_private(src_ip)

    @staticmethod
    def is_private(ip_address: str) -> str:
        is_private = False
        if ip_address != "":
            is_private = IpAddressHelper.is_private_ip(ip_address)

        return "1" if is_private else "0"
