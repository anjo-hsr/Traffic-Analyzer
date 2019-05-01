from main.helpers.combine_helper import CombineHelper


class DnsLookupEnricher:
    def __init__(self):
        self.header = "dst_query_name,dst_a_records,src_query_name,src_a_records"
        self.dns_responses = {}
        self.response_type_key = "1"
        self.a_record_key = "1"
        self.aaaa_record_key = "28"

    def is_response(self, packet):
        return packet["_ws.col.Protocol"] == "DNS" and packet["dns.flags.response"] == self.response_type_key

    def is_a_or_aaaa_response_type(self, dns_response_type):
        return dns_response_type == self.a_record_key or dns_response_type == self.aaaa_record_key

    @staticmethod
    def get_empty_dict(stream_id):
        return {
            "query_name": "",
            "a_records": [""],
            "stream_id": stream_id
        }

    def detect_dns_request(self, packet, stream_id):
        if self.is_response(packet):
            self.save_dns_query(packet)

        src_ip = packet["ip.src"]
        dst_ip = packet["ip.dst"]

        src_ip_information = self.dns_responses.get(src_ip, self.get_empty_dict(stream_id))
        src_a_records = CombineHelper.delimiter.join(src_ip_information["a_records"])
        src_ip_information = CombineHelper.delimiter.join(
            [src_ip_information["query_name"], src_a_records])

        dst_ip_information = self.dns_responses.get(dst_ip, self.get_empty_dict(stream_id))
        dst_a_records = CombineHelper.delimiter.join(dst_ip_information["a_records"])
        dst_ip_information = CombineHelper.delimiter.join(
            [dst_ip_information["query_name"], dst_a_records])

        combined_values = CombineHelper.delimiter.join([dst_ip_information, src_ip_information])
        if self.is_response(packet):
            self.write_file(packet, stream_id, combined_values)

        return combined_values

    def save_dns_query(self, packet):
        dns_response_types = packet["dns.resp.type"].split(",")
        if not any(self.is_a_or_aaaa_response_type(dns_response_type) for dns_response_type in dns_response_types):
            return

        dns_query_name = packet["dns.qry.name"]
        dns_response_names = packet["dns.resp.name"].split(",")
        dns_response_ips = packet["dns.a"].split(",") + packet["dns.aaaa"].split(",")

        filtered_dns_response_names = []

        for index, dns_response_type in enumerate(dns_response_types):
            if self.is_a_or_aaaa_response_type(dns_response_type) \
                    and not dns_response_names[index] in filtered_dns_response_names:
                filtered_dns_response_names.append(dns_response_names[index])

        for dns_response_ip in dns_response_ips:
            if dns_response_ip == "":
                continue

            self.dns_responses[dns_response_ip] = {
                "query_name": dns_query_name,
                "a_records": filtered_dns_response_names
            }

    @staticmethod
    def write_file(packet, stream_id, combined_values):
        dst_ip = packet["ip.dst"]
        src_ip = packet["ip.src"]
        cells = [stream_id, dst_ip, src_ip, combined_values]

        CombineHelper.delimiter.join(cells)
