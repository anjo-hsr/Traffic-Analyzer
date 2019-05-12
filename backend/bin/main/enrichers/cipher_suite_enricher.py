from main.helpers.print_helper import PrintHelper


class CipherSuiteEnricher:
    def __init__(self):
        self.header = "cipher_suite_number"
        self.stream_to_suites = {}

    def print(self):
        print_text = "Print out for all {} streams to cipher suites entries"
        PrintHelper.print_dict(self.stream_to_suites, print_text)

    def get_cipher_suite(self, packet):
        server_hello_identifier = "2"
        is_server_hello = packet["tls.handshake.type"] == server_hello_identifier
        cipher_suite_number = packet["tls.handshake.ciphersuite"]
        stream = packet["tcp.stream"]

        if cipher_suite_number != "" and is_server_hello:
            self.stream_to_suites[stream] = cipher_suite_number
            return cipher_suite_number

        if stream in self.stream_to_suites:
            return self.stream_to_suites[stream]

        return '""'
