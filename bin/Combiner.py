class Combiner:
    @staticmethod
    def get_src_dst(packet):
        dst_ip_addr = packet[4]
        src_ip_addr = packet[5]
        src_dst = [dst_ip_addr, src_ip_addr]
        return src_dst

    @staticmethod
    def combine_packet_information(joined_default_cells, locator, name_resolver, packet):
        src_dst = Combiner.get_src_dst(packet)
        fqdn_information = name_resolver.resolve(src_dst)
        location_information = locator.locate(src_dst)
        line = Combiner.combine_fields(joined_default_cells, fqdn_information, location_information)
        return line

    @staticmethod
    def combine_header(joined_default_cells, locator, name_resolver):
        fqdn_header = name_resolver.header
        location_header = locator.header
        line = Combiner.combine_fields(joined_default_cells, fqdn_header, location_header)
        return line

    @staticmethod
    def combine_fields(joined_default_cells, header_fqdn, header_location):
        return "{},{},{}".format(joined_default_cells, header_fqdn, header_location)

    @staticmethod
    def join_default_cells(packet, csv_delimiter):
        joined_default_cells = csv_delimiter.join('"{}"'.format(cell) for cell in packet)
        return joined_default_cells
