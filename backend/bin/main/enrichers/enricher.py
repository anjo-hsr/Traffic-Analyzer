from typing import Dict

from main.helpers.print_helper import PrintHelper


class Enricher(object):
    def __init__(self, enricher_type: str, header: str) -> None:
        self.enricher_type = enricher_type
        self.header = header

    def get_information(self, packet: Dict[str, str], information_dict) -> None:
        pass

    def print(self) -> None:
        PrintHelper.print_nothing(self.enricher_type)
