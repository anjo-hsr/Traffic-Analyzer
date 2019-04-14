from main.helpers.print_helper import PrintHelper


class TlsEnricher:

    def __init__(self):
        self.stream_to_handshake_version = {}
        self.header = "tls_ssl_version_negotiated"

    def get_tls_ssl_version(self, packet):
        server_hello_identifier = "2"
        is_server_hello = packet["tls.handshake.type"] == server_hello_identifier
        stream = packet["tcp.stream"]

        handshake_version = packet["tls.handshake.extensions.supported_version"]
        if handshake_version == "":
            handshake_version = packet["tls.handshake.version"]

        if handshake_version != "" and is_server_hello:
            self.stream_to_handshake_version[stream] = handshake_version
            return handshake_version

        if stream in self.stream_to_handshake_version:
            return self.stream_to_handshake_version[stream]

        return '""'

    def print(self):
        print_text = "Print out for {} streams to tls version entries"
        PrintHelper.print_dict(self.stream_to_handshake_version, print_text)
