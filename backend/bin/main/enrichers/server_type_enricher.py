from main.enrichers.enricher import Enricher
from main.helpers.combine_helper import CombineHelper


class ServerTypeEnricher(Enricher):
    def __init__(self):
        enricher_type = "server type enricher"
        header = "is_dhcp,is_dns"
        Enricher.__init__(self, enricher_type, header)

        self.dhcp_response_type_key = "2"
        self.dns_response_type_key = "1"
        self.server_type_dict = {"dns": set(), "dhcp": set()}

    def detect_server_type(self, packet) -> str:
        is_dhcp = self.detect_type(packet, self.is_dhcp_response, "dhcp")
        is_dns = self.detect_type(packet, self.is_dns_response, "dns")
        return CombineHelper.join_list_elements(is_dhcp, is_dns)

    def detect_type(self, packet, response_check, dict_key) -> str:
        is_type = False
        if response_check(packet):
            self.save_entry(dict_key, packet)
            is_type = True

        return str(is_type)

    def is_dns_response(self, packet) -> bool:
        return packet["_ws.col.Protocol"] == "DNS" and packet["dns.flags.response"] == self.dns_response_type_key

    def is_dhcp_response(self, packet) -> bool:
        return packet["_ws.col.Protocol"] == "DHCP" and packet["dhcp.option.dhcp"] == self.dhcp_response_type_key

    def save_entry(self, dict_key, packet) -> None:
        server_address = packet["ip.src"]
        self.server_type_dict[dict_key].add(server_address)
