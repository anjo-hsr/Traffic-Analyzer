from typing import Dict, Union, List

from main.enrichers.enricher import Enricher
from main.helpers.combine_helper import CombineHelper


class DnsLookupEnricher(Enricher):
    def __init__(self):
        enricher_type = "dns lookup enricher"
        header = "dst_query_name,dst_a_records,src_query_name,src_a_records"
        Enricher.__init__(self, enricher_type, header)

        self.dns_responses = {}
        self.response_type_key = "1"
        self.a_record_key = "1"
        self.aaaa_record_key = "28"

    def is_response(self, packet) -> bool:
        return packet["_ws.col.Protocol"] == "DNS" and packet["dns.flags.response"] == self.response_type_key

    def is_a_or_aaaa_response_type(self, dns_response_type) -> bool:
        return dns_response_type in [self.a_record_key, self.aaaa_record_key]

    @staticmethod
    def get_empty_dict(stream_id) -> Dict[str, Union[str, List[str]]]:
        return {
            "query_name": "",
            "a_records": [""],
            "stream_id": stream_id
        }

    def detect_dns_request(self, packet, stream_id) -> str:
        if self.is_response(packet):
            self.save_dns_query(packet)

        src_ip = packet["ip.src"]
        dst_ip = packet["ip.dst"]
        src_ip_information = self.generate_dns_information(src_ip, stream_id)
        dst_ip_information = self.generate_dns_information(dst_ip, stream_id)

        return CombineHelper.delimiter.join([dst_ip_information, src_ip_information])

    def generate_dns_information(self, src_ip, stream_id) -> str:
        src_ip_information = self.dns_responses.get(src_ip, self.get_empty_dict(stream_id))
        src_a_records = CombineHelper.delimiter.join(src_ip_information["a_records"])
        src_ip_information = CombineHelper.delimiter.join(
            [src_ip_information["query_name"], src_a_records])
        return src_ip_information

    def save_dns_query(self, packet) -> None:
        dns_response_types = packet["dns.resp.type"].split(",")
        if not any(self.is_a_or_aaaa_response_type(dns_response_type) for dns_response_type in dns_response_types):
            return

        dns_response_names = packet["dns.resp.name"].split(",")
        dns_query_name = packet["dns.qry.name"]
        dns_response_ips = packet["dns.a"].split(",") + packet["dns.aaaa"].split(",")

        filtered_dns_response_names = self.get_dns_response_names_set(dns_response_names, dns_response_types)
        self.write_dns_response_entry(dns_query_name, dns_response_ips, filtered_dns_response_names)

    def get_dns_response_names_set(self, dns_response_names, dns_response_types) -> set:
        filtered_dns_response_names = set()
        for index, dns_response_type in enumerate(dns_response_types):
            if self.is_a_or_aaaa_response_type(dns_response_type):
                filtered_dns_response_names.add(dns_response_names[index])

        return filtered_dns_response_names

    def write_dns_response_entry(self, dns_query_name, dns_response_ips, filtered_dns_response_names) -> None:
        for dns_response_ip in dns_response_ips:
            if dns_response_ip == "":
                continue

            self.dns_responses[dns_response_ip] = {
                "query_name": dns_query_name,
                "a_records": filtered_dns_response_names
            }
