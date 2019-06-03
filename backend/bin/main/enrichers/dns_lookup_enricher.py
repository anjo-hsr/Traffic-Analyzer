from typing import Dict, Union, List

from main.combiners.field_combiner import FieldCombiner
from main.enrichers.enricher import Enricher
from main.helpers.ip_helper import IpHelper
from main.helpers.response_helper import ResponseHelper
from main.helpers.string_helper import enclose_with_quotes


class DnsLookupEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "dns lookup enricher"
        header = "dst_query_name,dst_hostnames,src_query_name,src_hostnames"
        Enricher.__init__(self, enricher_type, header)

        self.dns_responses = {}
        self.a_record_key = "1"
        self.aaaa_record_key = "28"

    @staticmethod
    def get_empty_dict() -> Dict[str, Union[str, List[str]]]:
        return {
            "query_name": "",
            "hostnames": {""}
        }

    def get_information(self, packet, information_dict) -> None:
        if ResponseHelper.is_dns_response(packet):
            self.save_dns_query(packet)

        src_ip = packet["ip.src"]
        dst_ip = packet["ip.dst"]

        information_dict["dst_query_name"] = self.get_dns_query(dst_ip)
        information_dict["dst_hostnames"] = self.get_hostnames(dst_ip)

        information_dict["src_query_name"] = self.get_dns_query(src_ip)
        information_dict["src_hostnames"] = self.get_hostnames(src_ip)

        information_dict["domains"] = FieldCombiner.join_list_elements([
            information_dict["dst_query_name"],
            information_dict["dst_hostnames"],
            information_dict["src_query_name"],
            information_dict["src_hostnames"]
        ], True)

        information_dict["src_domains"] = FieldCombiner.join_list_elements([
            information_dict["src_query_name"],
            information_dict["src_hostnames"]
        ], True)

    def get_dns_query(self, ip) -> str:
        ip_information = self.dns_responses.get(ip, self.get_empty_dict())
        return enclose_with_quotes(ip_information["query_name"])

    def get_hostnames(self, ip) -> str:
        ip_information = self.dns_responses.get(ip, self.get_empty_dict())
        return FieldCombiner.join_with_quotes(ip_information["hostnames"])

    def save_dns_query(self, packet) -> None:
        dns_response_ips = packet["dns.a"].split(",") + packet["dns.aaaa"].split(",")
        filtered_dns_reponse_ips = list(filter(IpHelper.is_ip, dns_response_ips))
        if not filtered_dns_reponse_ips:
            return

        dns_response_names = packet["dns.resp.name"].split(",")
        dns_query_name = packet["dns.qry.name"]
        self.write_dns_response_entry(dns_query_name, filtered_dns_reponse_ips, dns_response_names)

    def write_dns_response_entry(self, dns_query_name, dns_response_ips, dns_hostnames) -> None:
        for dns_response_ip in dns_response_ips:
            self.dns_responses[dns_response_ip] = {
                "query_name": dns_query_name,
                "hostnames": dns_hostnames
            }
