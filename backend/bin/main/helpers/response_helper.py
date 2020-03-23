class ResponseHelper(object):
    @staticmethod
    def is_dns_response(packet) -> bool:
        dns_response_type_key = "1"
        return "DNS" in packet["_ws.col.Protocol"] and packet["dns.flags.response"] == dns_response_type_key

    @staticmethod
    def is_dhcp_response(packet) -> bool:
        dhcp_response_type_key = "2"
        return "DHCP" in packet["_ws.col.Protocol"] and packet["dhcp.option.dhcp"] == dhcp_response_type_key
