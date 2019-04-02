class CipherSuites:

    def __init__(self):
        self.stream_to_suites = {}
        self.header = "cipher_suite"

    def get_cipher_suite(self, packet):
        is_client_hello = packet["tls.handshake.ciphersuites"] == 1
        cipher_suite_number = packet["tls.handshake.ciphersuite"]
        stream = packet["tcp.stream"]
        if cipher_suite_number != "":
            if not is_client_hello:
                self.stream_to_suites[stream] = cipher_suite_number
                return cipher_suite_number

            if stream in self.stream_to_suites:
                return self.stream_to_suites[stream]


        return ""

    def print_fqdns(self):
        print("Print out for all {} stream to cipher suites entries".format(self.stream_to_suites.__len__()))
        for location_entry in self.stream_to_suites:
            print("{} --> {}".format(location_entry, self.stream_to_suites[location_entry]))

        print("\n\n")
