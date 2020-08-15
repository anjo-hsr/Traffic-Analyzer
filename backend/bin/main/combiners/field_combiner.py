from typing import List, Dict, Optional

from main.helpers.string_helper import enclose_with_quotes


class FieldCombiner(object):
    delimiter = ","

    @staticmethod
    def combine_packet_information(joined_default_cells: str, enriched_line: str) -> str:
        return FieldCombiner.join_list_elements([joined_default_cells, enriched_line])

    @staticmethod
    def join_list_elements(list_elements: List[str], quotes_needed: bool = False) -> str:
        if quotes_needed:
            return FieldCombiner.delimiter.join(enclose_with_quotes(list_element) for list_element in list_elements)

        return FieldCombiner.delimiter.join("{}".format(list_element) for list_element in list_elements)

    @staticmethod
    def join_default_cells(packet: Dict[str, str], field_names: Optional[List[str]]) -> str:
        return FieldCombiner.delimiter.join(enclose_with_quotes(packet[field_name]) for field_name in field_names)

    @staticmethod
    def join_with_quotes(fields: List[str]) -> str:
        return '"' + FieldCombiner.delimiter.join(fields) + '"'
