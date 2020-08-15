from typing import Dict, Union

from main.enrichers.enricher import Enricher
from main.helpers.print_helper import PrintHelper


class TlsVersionEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "tls version enricher"
        header = "tls_ssl_version_negotiated"
        Enricher.__init__(self, enricher_type, header)

        self.stream_to_handshake_version = {}

    def print(self) -> None:
        print_text = "Print out for {} streams to tls version entries"
        PrintHelper.print_dict(self.stream_to_handshake_version, print_text)

    def get_information(self, packet: Dict[str, str],
                        information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        server_hello_identifier = "2"
        is_server_hello = packet["tls.handshake.type"] == server_hello_identifier
        stream = information_dict["traffic_analyzer_stream"]

        handshake_version = packet["tls.handshake.extensions.supported_version"]
        if handshake_version == "":
            handshake_version = packet["tls.handshake.version"]

        if handshake_version != "" and is_server_hello:
            self.stream_to_handshake_version[stream] = handshake_version
            information_dict["tls_ssl_version_negotiated"] = handshake_version

        elif stream in self.stream_to_handshake_version:
            information_dict["tls_ssl_version_negotiated"] = self.stream_to_handshake_version[stream]

        else:
            information_dict["tls_ssl_version_negotiated"] = '""'
