from typing import Dict, Union

from main.enrichers.enricher import Enricher
from main.helpers.print_helper import PrintHelper


class TlsEstablishedEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "tls etablished enricher"
        header = "tls_is_established"
        Enricher.__init__(self, enricher_type, header)

        self.stream_to_tls_is_established_dict = {}

    def print(self) -> None:
        print_text = "Print out for {} streams to tls is established entries"
        PrintHelper.print_dict(self.stream_to_tls_is_established_dict, print_text)

    def get_information(self, packet: Dict[str, str],
                        information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        change_cipher_spec_identifier = "20"
        content_types = packet["tls.record.content_type"].split(",")
        is_change_cipher_spec = change_cipher_spec_identifier in content_types
        stream = information_dict["traffic_analyzer_stream"]

        if is_change_cipher_spec:
            self.stream_to_tls_is_established_dict[stream] = packet["_ws.col.Protocol"]

        elif stream in self.stream_to_tls_is_established_dict:
            packet["_ws.col.Protocol"] = self.stream_to_tls_is_established_dict[stream]

        information_dict["tls_is_established"] = "1" if stream in self.stream_to_tls_is_established_dict else "0"
