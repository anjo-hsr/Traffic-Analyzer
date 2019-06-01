import hashlib
from typing import Dict, Union

from main.enrichers.enricher import Enricher
from main.helpers.print_helper import PrintHelper


class StreamEnricher(Enricher):
    def __init__(self):
        enricher_type = "stream enricher"
        header = "traffic_analyzer_stream"
        Enricher.__init__(self, enricher_type, header)

        self.stream_ids = {"": ""}

    def print(self) -> None:
        print_text = "Print out for {} tcp stream entries"
        PrintHelper.print_dict(self.stream_ids, print_text)

    def get_information(self, packet, information_dict) -> None:
        inbound_outbound_string = self.get_combined_strings(packet)
        if inbound_outbound_string in self.stream_ids:
            information_dict["traffic_analyzer_stream"] = self.stream_ids[inbound_outbound_string]
            return

        stream_entry = self.generate_stream_id(inbound_outbound_string)

        self.stream_ids[stream_entry["combined_string"]] = stream_entry["stream_id"]
        information_dict["traffic_analyzer_stream"] = stream_entry["stream_id"]

    @staticmethod
    def get_combined_strings(packet) -> str:
        dst_ip = packet["ip.dst"]
        src_ip = packet["ip.src"]
        protocol = packet["ip.proto"]
        tcp_dst_port = packet["tcp.dstport"]
        tcp_src_port = packet["tcp.srcport"]
        udp_dst_port = packet["udp.dstport"]
        udp_src_port = packet["udp.srcport"]

        are_ports_set = (tcp_dst_port != "" and tcp_src_port != "") or \
                        (udp_dst_port != "" and udp_src_port != "")
        if not are_ports_set:
            return ""

        inbound = ",".join([dst_ip, src_ip, tcp_dst_port, tcp_src_port, udp_dst_port, udp_src_port, protocol])
        outbound = ",".join([src_ip, dst_ip, tcp_src_port, tcp_dst_port, udp_src_port, udp_dst_port, protocol])
        inbound_outbound_list = [inbound, outbound]
        inbound_outbound_list.sort()

        return ";".join(inbound_outbound_list)

    @staticmethod
    def generate_stream_id(combined_string) -> Dict[str, Union[str, int]]:
        hash_value = hashlib.sha256(combined_string.encode())
        stream_id = int(hash_value.hexdigest(), 16) % 100000000
        return {
            "combined_string": combined_string,
            "stream_id": stream_id
        }
