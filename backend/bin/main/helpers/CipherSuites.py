class CipherSuites:

    def __init__(self):
        self.stream_to_suites = {}
        self.header = "cipher_suite_number"

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

    def print(self):
        print("Print out for all {} stream to cipher suites entries".format(len(self.stream_to_suites)))
        for location_entry in self.stream_to_suites:
            print("{} --> {}".format(location_entry, self.stream_to_suites[location_entry]))

        print("\n\n")
