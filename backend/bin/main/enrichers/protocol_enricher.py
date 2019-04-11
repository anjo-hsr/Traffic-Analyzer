from main.helpers.print_helper import PrintHelper


class ProtocolEnricher:
    def __init__(self):
        self.header = "protocol"
        self.protocols = set([])

    def get_protocol(self, packet):
        protocols = packet["frame.protocols"]
        protocol_list = protocols.split(":")
        protocol = protocol_list[len(protocol_list) - 1]

        if protocol != "":
            self.protocols.add(protocol)

        return protocol

    def print(self):
        print_text = "Print out for all {} protocols"
        PrintHelper.print_list(self.protocols, print_text)