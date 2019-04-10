class ProtocolEnricher:
    def get_protocol(self, packet):
        protocols = packet["frame.protocols"]
        protocol_list = protocols.split(":")
        return protocol_list[len(protocol_list)]
