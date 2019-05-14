from main.helpers.print_helper import PrintHelper


class Enricher:
    def __init__(self, enricher_type, header):
        self.enricher_type = enricher_type
        self.header = header

    def print(self) -> None:
        PrintHelper.print_nothing(self.enricher_type)
