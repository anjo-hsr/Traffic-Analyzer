from typing import Dict


class CombineHelper:
    delimiter = ","

    @staticmethod
    def get_dst_src(packet) -> Dict[str, str]:
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src

    @staticmethod
    def combine_packet_information(joined_default_cells, enricher_jar, packet) -> str:
        ip_information_downloader = enricher_jar.ip_information_downloader
        dst_src = CombineHelper.get_dst_src(packet)
        dst_src_information = ip_information_downloader.get_dst_src_information(dst_src)

        information_dict = enricher_jar.get_information_dict(dst_src_information, packet)
        enriched_line = CombineHelper.delimiter.join(str(value) for value in information_dict.values())
        return CombineHelper.combine_fields([joined_default_cells, enriched_line])

    @staticmethod
    def combine_fields(fields, quotes_needed=False) -> str:
        if quotes_needed:
            return CombineHelper.delimiter.join('"{}"'.format(field) for field in fields)

        return CombineHelper.delimiter.join("{}".format(field) for field in fields)

    @staticmethod
    def join_default_cells(packet, field_names) -> str:
        return CombineHelper.delimiter.join('"{}"'.format(packet[field_name]) for field_name in field_names)
