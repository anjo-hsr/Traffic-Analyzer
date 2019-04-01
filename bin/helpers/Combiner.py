class Combiner:
    delimiter = ","

    @staticmethod
    def get_src_dst(packet):
        dst_ip_addr = packet["ip.dst"]
        src_ip_addr = packet["ip.src"]
        src_dst = [dst_ip_addr, src_ip_addr]
        return src_dst

    @staticmethod
    def combine_packet_information(joined_default_cells, locator, name_resolver, packet, timers):
        src_dst = Combiner.get_src_dst(packet)

        timers["fqdn"].start_lap()
        fqdn_information = name_resolver.resolve(src_dst)
        timers["fqdn"].end_lap()

        timers["location"].start_lap()
        location_information = locator.locate(src_dst)
        timers["location"].end_lap()

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
        return "{1}{0}{2}{0}{3}".format(Combiner.delimiter, joined_default_cells, header_fqdn, header_location)

    @staticmethod
    def join_default_cells(packet, csv_delimiter):
        joined_default_cells = csv_delimiter.join('"{}"'.format(packet[cell]) for cell in packet)
        return joined_default_cells

    @staticmethod
    def combine_fqdns(fqdns, destination, source):
        return "{1}{0}{2}".format(Combiner.delimiter, fqdns.get(destination), fqdns.get(source))

    @staticmethod
    def combine_lat_long(locations, destination):
        return Combiner.delimiter.join('"{}"'.format(cell) for cell in locations.get(destination))
