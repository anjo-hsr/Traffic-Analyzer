from main.enrichers.enricher import Enricher
from main.helpers.response_helper import ResponseHelper


class ServerTypeEnricher(Enricher):
    def __init__(self):
        enricher_type = "server type enricher"
        header = "is_dhcp,is_dns"
        Enricher.__init__(self, enricher_type, header)

        self.server_type_dict = {"dns": set(), "dhcp": set()}

    def get_information(self, packet, information_dict) -> None:
        information_dict["is_dhcp"] = self.detect_type(packet, ResponseHelper.is_dhcp_response, "dhcp")
        information_dict["is_dns"] = self.detect_type(packet, ResponseHelper.is_dns_response, "dns")

    def detect_type(self, packet, response_check, dict_key) -> str:
        is_type = False
        if response_check(packet):
            self.save_entry(dict_key, packet)
            is_type = True

        return str(is_type)

    def save_entry(self, dict_key, packet) -> None:
        server_address = packet["ip.src"]
        self.server_type_dict[dict_key].add(server_address)
