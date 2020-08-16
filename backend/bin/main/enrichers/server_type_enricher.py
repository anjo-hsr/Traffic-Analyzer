from typing import Dict, Union

from main.enrichers.enricher import Enricher
from main.helpers.domain_dict_helper import DomainDictHelper
from main.helpers.response_helper import ResponseHelper


class ServerTypeEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "server type enricher"
        header = "src_is_dhcp,src_is_dns,src_is_cdn,src_is_social_network"
        Enricher.__init__(self, enricher_type, header)

        self.server_type_dict = {
            "dns": set(),
            "dhcp": set(),
            "cdn": set(),
            "social_network": set()
        }

    def get_information(self, packet: Dict[str, str],
                        information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        information_dict["src_is_dhcp"] = self.detect_type(
            packet, information_dict, ResponseHelper.is_dhcp_response, "dhcp")
        information_dict["src_is_dns"] = self.detect_type(
            packet, information_dict, ResponseHelper.is_dns_response, "dns")

        information_dict["src_is_cdn"] = self.test_category(
            information_dict, "cdn")
        information_dict["src_is_social_network"] = self.test_category(
            information_dict, "social_network")

    def detect_type(self, packet: Dict[str, str], information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]],
                    response_check, dict_key) -> str:
        is_type = False
        if response_check(packet):
            self.save_entry(dict_key, information_dict)
            is_type = True

        return "1" if is_type else "0"

    def test_category(self,
                      information_dict: Dict[str, Union[str, Dict[str, Union[str, Dict[str, str], DomainDictHelper]]]],
                      key: str) -> str:
        domains = information_dict["src_domains"]
        domain_is_in_dict = information_dict["domain_dict_helpers"][key].check_domains(domains)
        if domain_is_in_dict:
            self.save_entry(key, information_dict)

        return "1" if domain_is_in_dict else "0"

    def save_entry(self, dict_key: str, information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        server_address = information_dict["ip_src_combined"]
        self.server_type_dict[dict_key].add(server_address)
