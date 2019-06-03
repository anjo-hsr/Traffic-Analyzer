from typing import Dict

from main.helpers.string_helper import enclose_with_quotes


class CombineHelper:
    delimiter = ","

    @staticmethod
    def get_dst_src(packet) -> Dict[str, str]:
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src

    @staticmethod
    def combine_packet_information(joined_default_cells, enriched_line) -> str:
        return CombineHelper.join_list_elements([joined_default_cells, enriched_line])

    @staticmethod
    def join_list_elements(list_elements, quotes_needed=False) -> str:
        if quotes_needed:
            return CombineHelper.delimiter.join(enclose_with_quotes(list_element) for list_element in list_elements)

        return CombineHelper.delimiter.join("{}".format(list_element) for list_element in list_elements)

    @staticmethod
    def join_default_cells(packet, field_names) -> str:
        return CombineHelper.delimiter.join(enclose_with_quotes(packet[field_name]) for field_name in field_names)

    @staticmethod
    def join_with_quotes(fields) -> str:
        return '"' + CombineHelper.delimiter.join(fields) + '"'
