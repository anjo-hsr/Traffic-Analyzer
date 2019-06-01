from main.dicts.cdn_dict import CdnDict
from main.enrichers.enricher import Enricher
from main.helpers.response_helper import ResponseHelper


class ServerTypeEnricher(Enricher):
    def __init__(self):
        enricher_type = "server type enricher"
        header = "src_is_dhcp,src_is_dns,src_is_cdn"
        Enricher.__init__(self, enricher_type, header)

        self.server_type_dict = {"dns": set(), "dhcp": set(), "cdn": set()}

    def get_information(self, packet, information_dict) -> None:
        information_dict["src_is_dhcp"] = self.detect_type(packet, ResponseHelper.is_dhcp_response, "dhcp")
        information_dict["src_is_dns"] = self.detect_type(packet, ResponseHelper.is_dns_response, "dns")
        information_dict["src_is_cdn"] = self.check_cdn(packet, information_dict)

    def detect_type(self, packet, response_check, dict_key) -> str:
        is_type = False
        if response_check(packet):
            self.save_entry(dict_key, packet)
            is_type = True

        return "1" if is_type else "0"

    def check_cdn(self, packet, information_dict) -> str:
        domains = information_dict["src_domains"]
        cdn_dict = CdnDict()
        is_cdn = cdn_dict.check_domains(domains)
        if is_cdn:
            self.save_entry("cdn", packet)

        return "1" if is_cdn else "0"

    def save_entry(self, dict_key, packet) -> None:
        server_address = packet["ip.src"]
        self.server_type_dict[dict_key].add(server_address)
