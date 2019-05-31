from main.enrichers.enricher import Enricher
from main.helpers.print_helper import PrintHelper


class CipherSuiteEnricher(Enricher):
    def __init__(self):
        enricher_type = "cipher_suite_enricher"
        header = "cipher_suite_number"
        Enricher.__init__(self, enricher_type, header)

        self.stream_to_suites = {}

    def print(self) -> None:
        print_text = "Print out for all {} streams to cipher suites entries"
        PrintHelper.print_dict(self.stream_to_suites, print_text)

    def get_information(self, packet, information_dict) -> None:
        server_hello_identifier = "2"
        is_server_hello = packet["tls.handshake.type"] == server_hello_identifier
        handshake_cipher_suite = packet["tls.handshake.ciphersuite"]
        stream = packet["tcp.stream"]

        cipher_suite_number = '""'

        if handshake_cipher_suite != "" and is_server_hello:
            self.stream_to_suites[stream] = handshake_cipher_suite
            cipher_suite_number = handshake_cipher_suite

        elif stream in self.stream_to_suites:
            cipher_suite_number = self.stream_to_suites[stream]

        information_dict["cipher_suite_number"] = cipher_suite_number
